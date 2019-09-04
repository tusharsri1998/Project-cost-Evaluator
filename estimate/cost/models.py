from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Employee(models.Model):
    emp_id = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    contact = models.CharField(max_length = 10)
    salary = models.IntegerField(default = 10000)
    def __str__(self):
        return str(self.emp_id)

class Project(models.Model):
    p_id = models.CharField(max_length=10,primary_key = True)
    p_name = models.CharField(max_length=30)



class Work(models.Model):
    empid = models.ForeignKey(Employee, related_name = 'employee', on_delete = models.CASCADE)
    pid = models.ForeignKey(Project, related_name = 'projects', on_delete = models.CASCADE)
    percent = models.FloatField()
    entry_date = models.DateField()
    flag = models.BooleanField(default=False)
    description = models.CharField(max_length=40)
    ind_cost = models.FloatField(default=0.0)


class Project_estimation(models.Model):
    projid = models.ForeignKey(Project, related_name = 'project', on_delete = models.CASCADE)
    cost = models.IntegerField(default = 0)

class Salary(models.Model):
    eid = models.ForeignKey(Employee,related_name='employid',on_delete=models.CASCADE)
    salary = models.IntegerField()
    date = models.DateField(auto_now=True)

class Concept(models.Model):
    concept_id = models.CharField(max_length= 15, primary_key = True)
    concept_name = models.CharField(max_length=30)
    approved = models.BooleanField(default = False)

class Concept_work(models.Model):
    c_id = models.ForeignKey(Concept, related_name='conceptid',on_delete=models.CASCADE)
    empl_id = models.ForeignKey(Employee, related_name = 'emplo', on_delete = models.CASCADE)
    hours = models.FloatField(null = True)
    date = models.DateField()
    desc = models.CharField(max_length=40)



# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Employee.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.employee.save()
