# Generated by Django 4.1.7 on 2023-02-28 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_attendance_time_in_alter_attendance_time_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
