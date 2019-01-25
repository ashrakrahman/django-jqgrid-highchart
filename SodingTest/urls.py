"""SodingTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from task.views import task_listview,home,create_task,task_updateview,delete_task,about_view,\
     task_listview_jqgrid,task_listview_high_chart
from accounts.views import login_view,regstration_view,logout_view

urlpatterns = [
    url(r'^$', home),
    url(r'^admin/', admin.site.urls),
    url(r'^about/', about_view),

    url(r'^login/', login_view,name='login'),
    url(r'^register/', regstration_view,name='registration'),
    url(r'^logout/', logout_view,name='logout'),

    url(r'^tasks/', task_listview,name='task_list'),
    url(r'^tasks-jq-grid/', task_listview_jqgrid,name='task_listview_jqgrid'),
    url(r'^tasks-high-chart/', task_listview_high_chart,name='task_listview_high_chart'),

    url(r'^edittasks/(?P<task_id>\d+)/', task_updateview,name='updatetasks'),
    url(r'^createtasks/', create_task,name='createtasks'),
    url(r'^deletetasks/(?P<task_id>\d+)/', delete_task,name='deletetasks'),
]
