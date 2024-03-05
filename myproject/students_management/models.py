# students_management/models.py

from django.db import models

class Standard(models.Model):
    standard_name = models.CharField(max_length=50)
    # Add any additional fields here

    def __str__(self):
        return self.standard_name

class Student(models.Model):
    name = models.CharField(max_length=100)
    rollno = models.IntegerField()
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    # Add any additional fields here

    def __str__(self):
        return self.name
