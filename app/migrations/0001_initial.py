# Generated by Django 4.1.7 on 2023-02-28 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('section', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('rollno', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('section', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=100)),
                ('phoneno', models.CharField(max_length=12)),
                ('encoding', models.TextField()),
                ('created', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_in', models.TimeField()),
                ('time_out', models.TimeField()),
                ('date', models.DateField()),
                ('rollno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student')),
            ],
        ),
    ]