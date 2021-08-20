# Generated by Django 3.2.5 on 2021-07-18 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0002_testrun_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='image_src',
            field=models.CharField(blank=True, default='https://source.unsplash.com/random', max_length=120),
        ),
        migrations.AlterField(
            model_name='answer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='option',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='test',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='testrun',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
