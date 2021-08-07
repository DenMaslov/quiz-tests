import logging
import os

from django.core.checks.messages import Error
from quiz import settings
from django.db.models import Q
from .forms import ModelForm
from django.utils import timezone
from django.shortcuts import redirect
from django.http.response import Http404, HttpResponse
from .models import Answer, Option, Test, Testrun
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import caches

cache = caches['views_cache']


log = logging.getLogger('app_info')


class TestListView(ListView):

    OLD_DATE = "1970-01-01 12:00:00"
    ORDER_FIELD = "created_at"

    model = Test
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(TestListView, self).get_context_data(**kwargs)
        context['form'] = ModelForm()
        return context

    def get_queryset(self):
        search = self.request.GET.get("search", None)
        suffix_order = self.request.GET.get("order", "")
        date_from, date_to = self.get_clean_time_ranges()

        #Return cached data for already searched query with same params
        cache_key = self.create_cache_key(search, date_from, date_to, suffix_order)
        data_from_cache = cache.get(cache_key)
        if data_from_cache:
            log.debug(f'Get cached data for key {cache_key}')
            return data_from_cache

        #If searching params are unique - cached new result, expiration - 10 minutes
        log.debug(f'Return Tests search: {search}; ranges: {date_from}, {date_to}')
        if search:
            tests = Test.objects.filter(Q(title_en__icontains=search) | Q(title_uk__icontains=search),
                                        created_at__range=[date_from, date_to]).order_by(
                suffix_order + self.ORDER_FIELD)
            cache.set(cache_key, tests, 60 * 10)
            return tests
        tests = Test.objects.filter(
            created_at__range=[date_from, date_to]).order_by(suffix_order + self.ORDER_FIELD)
        cache.set(cache_key, tests, 60 * 10)
        return tests

    def create_cache_key(self, search, date_from, date_to, suffix_order) -> str:
        """Creates simple key for caching"""
        search = str(search).replace(" ", '')
        date_from = str(date_from).replace(" ", '')
        date_to = str(date_to).replace(" ", '')[:12]
        return date_from + search + date_to + suffix_order

    def get_clean_time_ranges(self):
        """Returns date_from and date_to"""
        date_from = self.request.GET.get("from_date", self.OLD_DATE)
        date_to = self.request.GET.get("to_date", timezone.now())
        if date_to == "":
            date_to = timezone.now()
        if date_from == "":
            date_from = self.OLD_DATE
        return date_from, date_to


class TestDetailView(DetailView):
    model = Test
    template_name = 'tests/detail.html'

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        key = 'test-' + str(pk)

        # Get from cache if data exists in cache
        data_from_cache = cache.get(key)
        if data_from_cache:
            log.debug(f'Get cached data for key {key}')
            return data_from_cache

        # If cache does not have such obj - get from db and set to cache with termination 10 min
        try:
            test = Test.objects.get(pk=pk)
            cache.set(key, test, 60 * 10)
            return test
        except:
            raise Http404('There is not such obj')


class TestSessionView(LoginRequiredMixin, DetailView):
    login_url = "/auth/login/"
    model = Test
    template_name = 'tests/start.html'

    def post(self, request, **kwargs):
        test = Test.objects.get(pk=kwargs['pk'])
        self.create_test_session(request, test)
        return redirect('/')

    def create_test_session(self, request, test: Test) -> None:
        points = 0
        instance = Testrun.objects.create(
            test=test, user=self.get_user(request))
        for question in test.questions.all():
            answer_id = request.POST.get(str(question.id))
            if answer_id != None:
                user_option = Option.objects.get(id=answer_id)
                instance.answers.add(Answer.objects.create(user_answer=user_option,
                                                           question=question))
                if user_option == question.right_option:
                    points += 1
            else:
                instance.is_completed = False
        instance.points = points
        log.debug(
            f'Saving session: {instance.test}; {instance.user}; {instance.points}; {instance.finished_at}')
        instance.save()

    def get_user(self, request):
        if request.user.is_authenticated:
            return request.user
        return None


class TestSessionHistoryView(ListView):
    model = Testrun
    template_name = 'tests/history.html'

    def get_queryset(self):
        return Testrun.objects.filter(test__id=self.request.resolver_match.kwargs['pk']).order_by('-finished_at')
    ordering = ['-finished_at']


class TestScoreView(LoginRequiredMixin, ListView):
    login_url = "/auth/login/"
    permission_denied_message = 'To see your scores you should sign in first'
    model = Testrun
    template_name = 'tests/myscores.html'
    context_object_name = 'test_sessions'

    def get_queryset(self):
        return Testrun.objects.filter(user__id=self.request.user.id).order_by('-finished_at')


def download_file(request):
    filepath = settings.REPORT_FILE_PATH
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            resp = HttpResponse(
                file.read(), content_type="application/adminupload")
            resp['Content-Disposition'] = 'inline;filename=' + \
                os.path.basename(filepath)
            return resp
    raise Http404
