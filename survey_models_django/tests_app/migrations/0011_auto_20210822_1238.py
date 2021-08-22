# Generated by Django 3.2.5 on 2021-08-22 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0010_auto_20210810_0056'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestrunQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests_app.option')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testrunquestions', to='tests_app.question')),
            ],
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='answers',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.AddField(
            model_name='testrunquestions',
            name='testrun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testrunquestions', to='tests_app.testrun'),
        ),
        migrations.AddField(
            model_name='testrun',
            name='questions',
            field=models.ManyToManyField(related_name='testruns', through='tests_app.TestrunQuestions', to='tests_app.Question'),
        ),
    ]
