from django.db import models

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=200)
    rollno=models.CharField(max_length=12,primary_key=True)
    section=models.CharField(max_length=20)
    email=models.CharField(max_length=100)
    phoneno=models.CharField(max_length=12)
    encoding=models.TextField()
    created=models.DateTimeField(auto_now=True)

class Attendance(models.Model):
    rollno=models.ForeignKey(Student,on_delete=models.CASCADE)
    time_in=models.TimeField(blank=True)
    time_out=models.TimeField(blank=True)
    date=models.DateField(auto_now=True)

class Section(models.Model):
    section=models.CharField(max_length=20,primary_key=True)
    count=models.IntegerField()