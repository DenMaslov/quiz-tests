from django.contrib import admin
from .models import Option, Question, Test, Testrun, TestrunQuestions


class TestrunQuestionsAdmin(admin.ModelAdmin):
    model = TestrunQuestions
    list_display = ['question', 'testrun', 'answer']


class TestrunQuestionsInline(admin.TabularInline):
    model = Testrun.questions.through


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ['text', 'right_option']


class TestAdmin(admin.ModelAdmin):
    model = Test
    list_display = ['id', 'title', 'description', 'created_at']


class TestrunAdmin(admin.ModelAdmin):
    model = Testrun
    list_display = ['id', 'test', 'points','finished_at']
    inlines = [TestrunQuestionsInline]


admin.site.register(Option)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Testrun, TestrunAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestrunQuestions, TestrunQuestionsAdmin)
