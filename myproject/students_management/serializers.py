# students_management/serializers.py

from rest_framework import serializers
from .models import Student,Standard

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model=Standard
        fields='__all__'
