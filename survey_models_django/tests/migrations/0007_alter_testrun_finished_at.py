# Generated by Django 3.2.5 on 2021-07-19 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0006_auto_20210719_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testrun',
            name='finished_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]