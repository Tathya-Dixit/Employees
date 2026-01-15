from django.db import models

class Employee(models.Model):

    class Department(models.TextChoices):
        HR = 'HR',
        ENGINEERING = 'Engineering',
        SALES = 'Sales',
        NA = 'NA'

    class Role(models.TextChoices):
        DEVELOPER = 'Developer',
        MANAGER = 'Manager',
        ANALYST = 'Analyst',
        NA = 'NA'
    
    name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(unique=True, blank=False)

    department =  models.CharField(max_length=15, choices=Department.choices, blank=True)
    role = models.CharField(max_length=15, choices=Role.choices, blank=True)

    date_joined = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return self.name
