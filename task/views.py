import json
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Task
from django.views import View
from .forms import TaskCreateForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def home(request):
    template_name = 'home.html'
    return render(request,template_name,{})

@login_required(login_url='/login/')
def task_updateview(request, task_id):
    instance = get_object_or_404(Task,id=task_id)
    form = TaskCreateForm(request.POST or None, instance=instance)
    errors = None
    if form.is_valid() and request.user.is_authenticated():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/tasks/")
    if form.errors:
        errors = form.errors
    template_name = 'update_task.html'
    context = {
        "instance" : instance,
        "form" : form

    }
    return render(request,template_name,context)

@login_required(login_url='/login/')
def task_listview_high_chart(request):
    template_name = 'highchart.html'
    dataset_pie = [{
        'name': 'Chrome',
        'y': 61.41,
    }, {
        'name': 'Internet Explorer',
        'y': 11.84
    }, {
        'name': 'Firefox',
        'y': 10.85
    }, {
        'name': 'Edge',
        'y': 4.67
    }, {
        'name': 'Safari',
        'y': 4.18
    }]
    dataset_bar = [
              {'ticket_class': 1, 'survived_count': 200, 'not_survived_count': 123},
              {'ticket_class': 2, 'survived_count': 119, 'not_survived_count': 158},
              {'ticket_class': 3, 'survived_count': 181, 'not_survived_count': 528}
            ]
    categories = list()
    survived_series_data = list()
    not_survived_series_data = list()

    for entry in dataset_bar:
        categories.append('%s Class' % entry['ticket_class'])
        survived_series_data.append(entry['survived_count'])
        not_survived_series_data.append(entry['not_survived_count'])

    survived_series = {
        'name': 'Survived',
        'data': survived_series_data,
        'color': 'green'
    }

    not_survived_series = {
        'name': 'Not Survived',
        'data': not_survived_series_data,
        'color': 'red'
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Titanic Survivors by Ticket Class'},
        'xAxis': {'categories': categories},
        'series': [survived_series, not_survived_series]
    }

    dump = json.dumps(chart)

    return render(request, template_name, {'chart': dump , 'dataset_pie':json.dumps(dataset_pie)})

@login_required(login_url='/login/')
def task_listview(request):
    template_name = 'task_list_basic.html'
    user_id = request.user.id
    queryset = Task.objects.filter(taskuserid=user_id)
    context = {
        "object_list" : queryset
    }
    return render(request, template_name, context)


@login_required(login_url='/login/')
def task_listview_jqgrid(request):
    template_name = 'task_list.html'
    if request.is_ajax():
        page_number = request.GET.get('pagenum')
        page_size = request.GET.get('pagesize')
        start = int(page_number)*int(page_size)
        s = str(start)
        query = "select id,titel,description from task_task order by id limit "+s+","+page_size
        print query

        try:
            cur = connection.cursor()
            cur.execute(query)
            result = dictfetchall(cur)
            cur.close()
        except (Exception) as error:
            return HttpResponse(error, status=409)
        count = Task.objects.all().count()

        context = {
            'rows': result,
            'TotalRows': count
        }

        return HttpResponse(json.dumps(context), content_type='application/json')
    return render(request, template_name)


@login_required(login_url='/login/')
def create_task(request):
    form = TaskCreateForm(request.POST or None)
    errors = None
    if form.is_valid() and request.user.is_authenticated():
        instance = form.save(commit=False)
        instance.taskuserid = request.user.id
        instance.save()
        return HttpResponseRedirect ("/tasks/")
    if form.errors:
        errors = form.errors
    template_name = 'new_task.html'
    context = {
        "form":form,
        "errors":errors
    }
    return render(request,template_name,context)

@login_required(login_url='/login/')
def delete_task(request,task_id):
    instance = Task.objects.get(id=task_id)
    instance.delete()
    return HttpResponseRedirect("/tasks/")

@login_required(login_url='/login/')
def about_view(request):
    return render(request,"about.html",{})

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
