from django.shortcuts import render

from api.models import Employee
from api.serializers import EmployeeSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response


class EmployeeViewSet(viewsets.ModelViewSet):
    
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_fields = ['department', 'role']

