from .forms import ModelForm
from django.utils import timezone
from django.shortcuts import redirect
from .models import TestrunQuestions, Option, Test, Testrun
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


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
        order_field = self.get_order_field()
        date_from, date_to = self.get_clean_time_ranges()
        if search:
            return Test.objects.filter(title__icontains=search,
                                       created_at__range=[date_from, date_to]).order_by(
                order_field)
        return Test.objects.filter(
            created_at__range=[date_from, date_to]).order_by(order_field)

    def get_clean_time_ranges(self):
        """Returns date_from and date_to"""
        date_from = self.request.GET.get("from_date", self.OLD_DATE)
        date_to = self.request.GET.get("to_date", timezone.now())
        if date_to == "":
            date_to = timezone.now()
        if date_from == "":
            date_from = self.OLD_DATE
        return date_from, date_to

    def get_order_field(self) -> str:
        """Returns orderfield"""
        prefixes_order = self.request.GET.get("order", "")
        return prefixes_order + self.ORDER_FIELD


class TestDetailView(DetailView):
    model = Test
    template_name = 'tests/detail.html'


class TestSessionView(DetailView):
    model = Test
    template_name = 'tests/start.html'

    def post(self, request, **kwargs):
        test = Test.objects.get(pk=kwargs['pk'])
        self.create_test_session(request, test)
        return redirect('/')

    def create_test_session(self, request, test: Test) -> None:
        instance = Testrun.objects.create(test=test, user=self.get_user(request))
        for question in test.questions.all():
            answer_id = request.POST.get(str(question.id))
            if answer_id is not None:
                user_option = Option.objects.get(id=answer_id)
                is_answer_right = user_option == question.right_option
                TestrunQuestions.objects.create(testrun=instance,
                                                question=question,
                                                answer=user_option,
                                                is_right=is_answer_right)
        instance.update_points()

    def get_user(self, request):
        if request.user.is_authenticated:
            return request.user
        return None


class TestSessionHistoryView(ListView):
    model = Testrun
    template_name = 'tests/history.html'

    def get_queryset(self):
        return Testrun.objects.filter(
            test__id=self.request.resolver_match.kwargs['pk']).order_by('-finished_at')


class TestScoreView(LoginRequiredMixin, ListView):
    login_url = "/auth/login/"
    permission_denied_message = 'To see your scores you should sign in first'
    model = Testrun
    template_name = 'tests/myscores.html'
    context_object_name = 'test_sessions'

    def get_queryset(self):
        return Testrun.objects.filter(
                user__id=self.request.user.id).order_by('-finished_at')
