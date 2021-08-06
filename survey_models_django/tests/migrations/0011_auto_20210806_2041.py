# Generated by Django 3.2.6 on 2021-08-06 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0010_auto_20210804_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='description_en',
            field=models.CharField(blank=True, max_length=280, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='description_uk',
            field=models.CharField(blank=True, max_length=280, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='title_en',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='test',
            name='title_uk',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]