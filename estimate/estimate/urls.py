"""estimate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from django.conf.urls import include
from django.contrib.auth import views as auth_views

from cost import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.test , name = 'test')
    path('project/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('project/workdone/', views.workdone , name = 'workdone'),
    # path('project/workdone/data_transfer', views.data_transfer, name = 'data_transfer'),

    path('project/login_success/', views.login_success , name = 'login_success'),

    path('project/new_project/',views.new_project,name='new_project'),
    path('project/add_project/',views.add_project,name='add_project'),
    path('project/add_employee/',views.add_employee,name='add_employee'),
    path('project/new_employee/',views.new_employee,name='new_employee'),
    path('project/project_code/',views.project_code,name='project_code'),
    path('project/fucking_calculations',views.fucking_calculations,name="fucking_calculations"),
    path('project/getcost',views.getcost,name='getcost'),
    path('project/workdone/data_test',views.data_test,name='data_test'),
    path('project/login_success/data_test',views.data_test,name='data_test'),
    # path('export/csv/', views.export_users_csv, name='export_users_csv'),
    path('project/number_days',views.number_days,name='number_days'),
    path('project/new_salary', views.new_salary, name='new_salary'),
    path('project/change_salary/', views.change_salary, name='change_salary'),
    path('project/concept', views.concept, name = "concept"),
    path('project/choose', views.choose, name = "choose"),
    path('project/concept_code/',views.concept_code,name='concept_code'),
    path('project/workdone/concept_test',views.concept_test,name='concept_test'),
    path('project/new_concept/',views.new_concept,name='new_concept'),
    path('project/add_concept/',views.add_concept,name='add_concept'),
    path('project/project_name/',views.project_name,name='project_name'),
    path('project/concept_name/',views.concept_name,name='concept_name'),
    path('project/workdone/todo_list',views.todo_list,name = 'todo_list'),
    path('project/dayswork',views.dayswork, name="dayswork"),
    path('project/anyday',views.anyday, name="anyday"),
    path('project/getdate',views.getdate, name="getdate"),
    path('project/send1',views.send1,name='send1'),
    path('project/missed',views.missed, name='missed'),
    path('project/missed1',views.missed1, name='missed1'),
    path('project/left', views.left, name='left'),
    path('project/right',views.right,name='right')
    # path('project/every_10_seconds', views.every_10_seconds, name="every_10_seconds")


    # path('export1/csv',views.get_summary,name='get_summary'),


]
