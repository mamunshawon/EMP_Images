from .views import *
from django.urls import path

urlpatterns = [
    path('add-employee', add_employee, name='add_employee'),
    path('login', user_login, name='user-login'),
    path('logout', user_logout, name='user_logout'),
    path('add-daily-task', add_daily_report, name ='add_task'),
    path('leave-form', leave_form, name='leave_form'),
    path('proposals', proposals, name='proposals'),
    path('proposals_evaluation/<status>/<id>', proposals_evaluation, name='proposals_evaluation'),
    path('home_page', home_page, name='home_page'),
    path('my_leave', my_leave_report, name='my_leave'),
    path('my-todolist', my_todolist, name='my_todolist'),
    path('punch_in', punch_in, name='punch_in'),
    path('move-todo-list/<id>/<sts>', move_todo_list, name='move_todo_list'),
    path('add-to-list', add_to_list, name='add-to-list'),
    path('my-profile', my_profile, name='my_profile'),
    path('change-password', change_password, name='change-password')

]