from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Employee, Project, Work, Project_estimation, Salary, Concept, Concept_work
from django.contrib.auth.models import User
from datetime import date
import datetime
from .forms import newform
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.csrf import csrf_protect
from django.core import serializers
from django.db.models import Q
from django.db.models import F
from django.db import transaction
import csv
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from io import StringIO
from celery.schedules import crontab
from celery.task import periodic_task
from datetime import timedelta



# Create your views here.


@login_required
def workdone(request):
    project = Project.objects.all()
    concept = Concept.objects.all()
    xx = Employee.objects.get(emp_id = request.user)
    # ls=[]
    ti = Work.objects.all().filter(empid=xx,entry_date = date.today())
    print(ti)
    ls = Work.objects.filter(empid=xx, entry_date = date.today()).values_list('pid',flat = True)
    ls1 = Work.objects.filter(empid=xx, entry_date = date.today()).values_list('percent',flat = True)
    # & Q(entry_date=date.today)
    return render(request, 'datatest.html', {'project': project, 'concept':concept, 'ti':ti})

@csrf_protect
def missed(request):
        # for i in range(len(empl)):
    project = Project.objects.all()
    user = User.objects.all()

    return render(request, 'missed.html', {'project': project, 'user':user})

@csrf_protect
def missed1(request):
    concept = Concept.objects.all()
    user = User.objects.all()
    return render(request, 'missed1.html', {'concept':concept, 'user':user})

@csrf_protect
def left(request):
    if request.method=="POST":
        empl = request.POST.getlist('empid')
        code = request.POST.getlist('code')
        hour = request.POST.getlist('hours')
        desc = request.POST.getlist('description')
        date = request.POST.get('date')
        print(empl, code, hour)
        # yy = Employee.objects.filter(emp_id = request.user).values_list('emp_id', flat = True)
        # print(yy)
        for i in range(len(empl)):
            zz = User.objects.filter(username = empl[i]).values_list('id', flat = True)
            userid  = Employee.objects.get(emp_id = zz[0])
            print(userid)
            projid = Project.objects.get(p_id = code[i])
            ins = Work.objects.create(empid = userid,pid = projid,percent = hour[i],entry_date = date, description = desc[i])
        print('entry success')
    return HttpResponseRedirect('login_success/')
    # return render(request,'admin_page.html')
@csrf_protect
def right(request):
    print(request.POST)
    if request.method=="POST":
        empl = request.POST.getlist('empid1')
        code = request.POST.getlist('code1')
        hour = request.POST.getlist('hours1')
        desc = request.POST.getlist('description1')
        date = request.POST.get('date')
        # yy = Employee.objects.filter(emp_id = request.user).values_list('emp_id', flat = True)
        # print(yy)
        for i in range(len(empl)):
            projcode = Concept.objects.get(concept_id = code[i])
            zz = User.objects.filter(username = empl[i]).values_list('id', flat = True)
            userid  = Employee.objects.get(emp_id = zz[0])
            ins = Concept_work.objects.create(c_id = projcode,empl_id = userid,hours = hour[i], date = date, desc = desc[i])
        print('entry success in concept')
    return HttpResponseRedirect('login_success/')
    # return render(request,'admin_page.html')

def choose(request):
    return render(request , 'choose.html')

def concept(request):
    concept = Concept.objects.all()
    return render(request, 'concept.html',{'concept':concept})

@csrf_exempt
def concept_code(request):
    p = json.loads(request.body)
    print(p)
    # data = request.POST['projId']
    proj_name = Concept.objects.filter(concept_id=p).values_list('concept_name',flat = True)
    # send_data = serializers.serialize('json', list(proj_code))
    print(proj_name[0])
    return HttpResponse(proj_name)

@csrf_exempt
def concept_name(request):
    t = json.loads(request.body)
    print(t)
    # data = request.POST['projId']
    proj_code = Concept.objects.filter(concept_name=t).values_list('concept_id',flat = True)
    # send_data = serializers.serialize('json', list(proj_code))
    print(proj_code[0])
    return HttpResponse(proj_code)

@csrf_protect
def concept_test(request):
    if request.method=='POST':
        code = request.POST.getlist('a[]')
        print(code)
        hours = request.POST.getlist('aa[]')
        print(hours)
        des = request.POST.getlist('aaa[]')
        userid = Employee.objects.get(emp_id = request.user)
        print(type(userid))
        for i in range(len(code)):
            projcode = Concept.objects.get(concept_id = code[i])
            print(projcode,hours[i],userid)
            ins = Concept_work.objects.create(c_id = projcode,empl_id = userid,hours = hours[i], date = date.today(), desc = des[i])
        print('bye')
        return render(request,'home.html')

@csrf_exempt
def project_code(request):
    p = json.loads(request.body)
    print(p)
    # data = request.POST['projId']
    proj_code = Project.objects.filter(p_id=p).values_list('p_name',flat = True)
    # send_data = serializers.serialize('json', list(proj_code))
    print(proj_code[0])
    return HttpResponse(proj_code)

@csrf_exempt
def project_name(request):
    t = json.loads(request.body)
    print(t)
    # data = request.POST['projId']
    proj_code = Project.objects.filter(p_name=t).values_list('p_id',flat = True)
    # send_data = serializers.serialize('json', list(proj_code))
    print(proj_code[0])
    return HttpResponse(proj_code)

def test(request):
    employee = Employee.objects.all()
    users = User.objects.all().select_related('employee')

    return render(request, 'test.html', {'users': users})

@login_required
@csrf_protect
def data_transfer(request):

    # if request.method=='POST':
        print("hi")
        # rowcount = request.POST.getlist('data')
        # print(rowcount)
        code = request.POST.get('code')
        projectObject = Project.objects.get(p_id=code)
        proj = projectObject.p_id
        # print(proj)
        # print(type(proj))
        percent = request.POST.get('percent')
        # print(type(request.user))
        userid = Employee.objects.get(emp_id = request.user)
        print(date.today())
        work_obj = Work(empid = userid, pid = projectObject, percent = percent, entry_date = date.today())
        work_obj.save()
        return HttpResponseRedirect('/')
#

@csrf_protect
def data_test(request):
    if request.method=='POST':

        code = request.POST.getlist('v[]')
        print(code)
        hours = request.POST.getlist('vv[]')
        print(hours)
        des = request.POST.getlist('vvv[]')
        print(des)
        print(type(request.user))
        userid = Employee.objects.get(emp_id = request.user)
        for i in range(len(code)):
            print(type(code[i]))
            projcode = Project.objects.get(p_id = code[i])
            print(type(projcode))
            print(projcode,hours[i],userid)
            ins = Work.objects.create(empid = userid,pid = projcode,percent = hours[i],entry_date = date.today(), description = des[i])

        print('bye')
        return render(request,'home.html')


def login_success(request):
    if(request.user.is_superuser):
       return render(request, 'admin_page.html')
    else:
        project = Project.objects.all()
        concept = Concept.objects.all()
        return render(request, 'datatest.html',{'project':project, 'concept': concept})

@login_required
def add_project(request):
    if(request.method=='POST'):
        code=request.POST.get('code')
        name=request.POST.get('project')
        proj_obj = Project( p_id = code, p_name = name)
        proj_obj.save()
        return render(request, 'admin_page.html')

@login_required
def add_concept(request):
    if(request.method=='POST'):
        code=request.POST.get('code')
        name=request.POST.get('concept')
        proj_obj = Concept( concept_id = code, concept_name = name)
        proj_obj.save()
        return render(request, 'admin_page.html')

@login_required
def new_project(request):
     return render(request,'new_project.html')

@login_required
def new_concept(request):
     return render(request,'new_concept.html')

@login_required
def new_employee(request):
    return render(request,'new_employee.html')


@login_required
def add_employee(request):
    if(request.method=='POST'):
        id = request.POST.get('id')
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        contact = request.POST.get('contact')
        u = User.objects.create_user(
            username=id,
            password=str(id)+'@1234',
            first_name=fname,
            last_name=lname,
        )
        k = Employee.objects.create(
            emp_id=User.objects.get(username=id),
            contact=contact,
        )
        return render(request, 'admin_page.html')

def getcost(request):
    project = Project.objects.all()
    return render(request,'getcost.html',{'project':project})

def fucking_calculations(request):
    if request.method=="POST":
        code = request.POST.get('code')
        codeobj = Project.objects.get(p_id=code)
        code1 = codeobj.p_id
        Work.objects.filter(pid=codeobj).update(flag=False)
        ls=Work.objects.filter(
        Q(pid=codeobj) & Q(flag=False)
        ).values_list('empid','percent')
        ls1=[]
        if ls:
            for i in range(ls.count()):
                # pz = User.objects.filter(id=ls[i][0]).values_list('username')
                # print(pz[0])
                p1 = Employee.objects.filter(emp_id=ls[i][0]).values_list('salary', flat=True)
                print(p1[0])
                ls1.append(p1[0])
        print(ls1)
        cost=0
        # emp = User.objects.values_list('id',flat=True)
        for j in range(ls.count()):
            cost = cost + ls[j][1]*ls1[j]/(20*9)
        print(cost)
        estobj = Project_estimation.objects.filter(projid=codeobj).values_list('cost',flat = True)
        if estobj:
            Project_estimation.objects.filter(projid=codeobj).update(cost=cost)
        if ls:
            for p in range(ls.count()):
                Work.objects.filter(pid=codeobj).update(flag=True)
        estobj = Project_estimation.objects.filter(projid=codeobj).values_list('cost',flat = True)
        s = estobj[0]
        return HttpResponse('Total cost of project till date = {}'.format(s))
        # return HttpResponse('Total cost of project till date =')


def number_days(request):
    if(request.method=='POST'):
        code = request.POST.get('code')
        codeobj = Project.objects.get(p_id=code)
        code1 = codeobj.p_id

        count_days=[]
        x = Work.objects.filter(pid=codeobj).values_list('empid','pid','percent')
        indi_cost=[]
        emp_list=[]
        p = Employee.objects.all().values_list('emp_id','salary')
        emp_ls=set()
        for i in range(len(p)):
            cost1=0
            sum = 0
            y = Work.objects.filter(Q(empid=p[i])&Q(pid=codeobj)).values_list('empid','pid','percent')
            if (y.count()!=0):
                for k in range(y.count()):
                    sum+=y[k][2]
                    emp_list.append(y[k][0])
                    l = Employee.objects.filter(emp_id=y[k][0]).values_list('salary',flat=True)
                    print(l[0])
                    cost1 += y[k][2]*l[0]/(20*9)
                indi_cost.append(cost1)
                count_days.append(sum)
                emp_ls = set(emp_list)
        print(emp_ls,count_days,indi_cost)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="summary.csv"'
        writer = csv.writer(response)
        writer.writerow(['Employee ID','Name','Number of hours','Individual Cost'])
        ls = list(emp_ls)
        print(ls)
        ls_user=[]
        ls_first=[]
        for r in range(len(count_days)):
            w = User.objects.filter(id=ls[r]).values_list('username',flat=True)
            b = User.objects.filter(id=ls[r]).values_list('first_name',flat=True)
            ls_user.append(w[0])
            ls_first.append(b[0])
        for l in range(len(count_days)):
            row = [ls_user[l],ls_first[l], count_days[l],indi_cost[l]]
            writer.writerow(row)
        # ls_user[l][0],ls_user[l][1],
        return response
        # get_summary(emp_ls,count_days,indi_cost)
    return render(request, 'getcost.html')

def change_salary(request):
    if request.method=='POST':
        p = request.POST.get('employee')
        x = User.objects.filter(username = p).values_list('id',flat = True)
        print(x,type(x))
        y = Employee.objects.get(emp_id_id = x[0])
        print(type(y))
        sal=request.POST.get('salary')
        salary_obj = Salary.objects.create(eid=y,salary=sal, date=date.today())

        return render(request,'admin_page.html')


def new_salary(request):
    employee = Employee.objects.all()
    return render(request,'change_salary.html',{'employee': employee})

def todo_list(request):
    user = Employee.objects.get(emp_id = request.user)
    print(user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="todo_list.csv"'
    writer = csv.writer(response)
    writer.writerow(['Project ID','Description','Date'])
    x=[]
    y=[]
    x.append(Work.objects.filter(empid = user).values_list('pid','description', 'entry_date'))
    y.append(Concept_work.objects.filter(empl_id=user).values_list('c_id','desc','date'))
    print(len(x[0]))
    if x[0] or y[0]:
        if x[0]:
            for i in range(len(x[0])):
                row = [x[0][i][0],x[0][i][1], x[0][i][2]]
                print(x[0][i][0],x[0][i][1], x[0][i][2])
                writer.writerow(row)
            writer.writerow(['','',''])
        if y[0]:
            for j in range(len(y[0])):
                row = [y[0][j][0],y[0][j][1], y[0][j][2]]
                print(y[0][j][0],y[0][j][1], y[0][j][2])
                writer.writerow(row)
        return response

    else:
        return HttpResponse('You havent worked on any project yet')

def anyday(request):
    return render(request, 'anyday.html')

def getdate(request):
    if request.method =='POST':
        date = request.POST.get('datee')
        ls=[]
        ls1=[]
        ls.append(Work.objects.filter(entry_date = date).values_list('empid','pid', 'percent', 'description'))
        ls1.append(Concept_work.objects.filter(date = date).values_list('empl_id','c_id', 'hours', 'desc'))
        print(ls1[0])
        if ls[0] or ls1[0]:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="particular_date.csv"'
            writer = csv.writer(response)
            writer.writerow(['Employee','Project Id', 'Hours', 'Description'])
            if ls[0]:
                # print('ye chal rha')
                for i in range(len(ls[0])):
                    p = User.objects.filter(id = ls[0][i][0]).values_list('first_name', flat = True)
                    row = [p[0], ls[0][i][1], ls[0][i][2], ls[0][i][3]]
                    writer.writerow(row)
            if ls1[0]:
                writer.writerow(['','','',''])
                # print('ye bhi chal rha')
                for i in range(len(ls1[0])):
                    p = User.objects.filter(id = ls1[0][i][0]).values_list('first_name', flat = True)
                    row = [p[0], ls1[0][i][1], ls1[0][i][2], ls1[0][i][3]]
                    writer.writerow(row)

            return response
        else:
            return HttpResponse('No entry for the given date')
    return render(request, 'admin_page.html')

def dayswork(request):
    p=[]
    q=[]
    print(date.today)
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    p.append(Work.objects.filter(entry_date__range=(today_min, today_max)).values_list('empid','pid','percent', 'description'))
    q.append(Concept_work.objects.filter(date__range=(today_min, today_max)).values_list('empl_id','c_id','hours', 'desc'))
    print(p[0])
    ls=[]
    ls1=[]
    if p[0]:
        for i in range(len(p[0])):
            z = User.objects.filter(id = p[0][i][0]).values_list('first_name',flat = True)
            ls.append(z[0])
    if q[0]:
        for j in range(len(q[0])):
            t = User.objects.filter(id = q[0][i][0]).values_list('first_name',flat = True)
            ls1.append(t[0])
    response = HttpResponse(content_type='text/csv')
    csvfile = StringIO()
    response['Content-Disposition'] = 'attachment; filename="daily_list.csv"'
    writer1 = csv.writer(response)
    writer = csv.writer(csvfile)
    writer.writerow(['Employee name','Project Id','Description', 'No. of Hours'])
    writer1.writerow(['Employee name','Project Id','Description', 'No. of Hours'])
    if p[0] or q[0]:
        if p[0]:
            for i in range(len(p[0])):
                row = [ls[i],p[0][i][1],p[0][i][3], p[0][i][2]]
                writer.writerow(row)
                writer1.writerow(row)
            writer.writerow(['','','',''])
            writer1.writerow(['','','',''])
        if q[0]:
            for i in range(len(q[0])):
                row = [ls1[i],q[0][i][1],q[0][i][3], q[0][i][2]]
                writer.writerow(row)
                writer1.writerow(row)
        email = EmailMessage(
        'Django csv file attached',
        'PFA daily work csv file',
        settings.EMAIL_HOST_USER,
        ['rajat@smartivity.in'],
        )
        email.attach('file.csv', csvfile.getvalue(), 'text/csv')
        email.send()
        print('kuch to hua hai')
        return response
    else:
        return HttpResponse('No work submitted today by employees')

# def concwork(request):
#     t=[]


def send1(request):
    subject = 'tumhari lulli choti h'
    message = 'Pant chudai machane jaa rha iss weekend gurgaon!!!'
    from_email = settings.EMAIL_HOST_USER
    to_list = ['2016014@iiitdmj.ac.in', '2016285@iiitdmj.ac.in', '2016011@iiitdmj.ac.in']
    send_mail(subject, message, from_email, to_list, fail_silently=False)
    return render(request,'admin_page.html')

# '2016295@iiitdmj.ac.in', '2016255@iiitdmj.ac.in', '2016101@iiitdmj.ac.in', '2016104@iiitdmj.ac.in', '2016106@iiitdmj.ac.in', '2016186@iiitdmj.ac.in','2016176@iiitdmj.ac.in', '2016030@iiitdmj.ac.in', '2016162@iiitdmj.ac.in', '2016048@iiitdmj.ac.in', '2016049@iiitdmj.ac.in', '2016078@iiitdmj.ac.in', '2016162@iiitdmj.ac.in'
# def new_concept(request):
