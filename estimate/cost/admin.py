from django.contrib import admin

# Register your models here.
from .models import (Employee, Project, Work, Project_estimation, Salary, Concept, Concept_work )

admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(Work)
admin.site.register(Project_estimation)
admin.site.register(Salary)
admin.site.register(Concept)
admin.site.register(Concept_work)
# Concept, Concept_work
