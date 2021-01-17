from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages


# Create your views here.
@login_required(login_url='/login')
def add_employee(request):
    user = request.user
    user = User.objects.get(username=user)
    print(user)
    u = user.groups.filter(name='HR').exists()
    if u:
        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST['password']
            gender = request.POST['gender']
            role = request.POST['role']
            email = request.POST['email']
            department = request.POST['department']
            print(role)
            print(department)
            user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                            last_name=last_name, email=email)
            group = Group.objects.get(id=role)
            print(group.name)
            user.groups.add(group)
            user.save()
            department = Department.objects.get(id=department)
            print(department.name)
            Profile.objects.create(user=user, department=department)
            return HttpResponse('Done')
        else:
            form = UserForm()
            context = {'form': form}
            return render(request, 'user_creation_form.html', context)

    else:
        message = "Server Error!"
        context = {'message': message}
        return render(request, 'message.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/home_page')
    form = UserLoginForm()
    context = {'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def add_daily_report(request):
    if request.method == 'POST':
        form = DailyTaskForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            user = request.user
            form.user = user
            form.save()
            return HttpResponse("successfully added")

    form = DailyTaskForm()
    context = {'form': form}
    return render(request, 'add-task.html', context)


@login_required(login_url='/login')
def leave_form(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return HttpResponse('Successfully Added')
    form = LeaveForm()
    context = {'form': form}
    return render(request, 'leave_form.html', context)


@login_required(login_url='/login')
def proposals(request):
    if request.user.groups.filter(name='HR').exists():
        try:
            proposals = Leave.objects.filter(checked_in=False)
            if proposals:
                context = {'proposals': proposals}
                return render(request, 'proposals.html', context)
            else:
                message = "No Applications are available"
                context = {'message': message}
                return render(request, 'proposals.html', context)
        except:
            message = "No Applications are available"
            context = {'message': message}
            return render(request, 'proposals.html', context)
    else:
        message = "server Error!"
        context = {'message': message}
        return render(request, 'proposals.html', context)


@login_required(login_url='/login')
def proposals_evaluation(request, status, id):
    proposals = Leave.objects.get(id=id)
    proposals.status = status
    proposals.checked_in = 1
    proposals.save()
    return HttpResponse("Ok")


@login_required(login_url='/login')
def my_leave_report(request):
    if request.user.is_authenticated:
        my_application = Leave.objects.filter(user=request.user)
        context = {'my_application': my_application}
        return render(request, 'my_application.html', context)
    else:
        return redirect("/login")


@login_required(login_url='/login')
def my_profile(request):
    if request.user.is_authenticated:

        try:
            user = request.user
            print(user)
            if user:
                profile = Profile.objects.get(user=user)
                context = {'profile': profile}
                print('asdeeu')
                return render(request, 'profile.html', context)
        except:
            message = "user is not logged in"
            context = {'message': message}
            return render(request, 'profile.html', context)
    else:
        return redirect("/login")


def home_page(request):
    return render(request, 'home.html')


@login_required(login_url='/login')
def my_todolist(request):
    if request.user.is_authenticated:
        user = request.user
        pending_todo_list = TodoList.objects.filter(user=user, pending_status=True)
        working_todo_list = TodoList.objects.filter(user=user, working_status=True)
        done_todo_list = TodoList.objects.filter(user=user, done_status=True)
        context = {'pending_todo_list': pending_todo_list, 'working_todo_list': working_todo_list,
                   'done_todo_list': done_todo_list}
        return render(request, 'my_todo_list.html', context)
    else:
        return redirect('/login')


@login_required(login_url='/login')
def punch_in(request):
    if request.method == 'POST':
        form = PunchInForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            user = request.user
            form.user = user
            form.save()
            return HttpResponse("successfully added")

    form = PunchInForm()
    context = {'form': form}
    return render(request, 'punch_in.html', context)


@login_required(login_url='/login')
def move_todo_list(request, id, sts):
    to_do_list = TodoList.objects.get(id=id)
    if sts == 'done':
        to_do_list.done_status = True
        to_do_list.working_status = True
        to_do_list.pending_status = True
        to_do_list.save()
        return redirect('/my-todolist')
    elif sts == 'working':
        to_do_list.working_status = True
        to_do_list.pending_status = False
        to_do_list.done_status = False
        to_do_list.save()
        return redirect('/my-todolist')


@login_required(login_url='/login')
def add_to_list(request):
    if request.method == 'POST':
        what_to = request.POST['what-to-do']
        when_to = request.POST['when-to-do']
        create_todo_list = TodoList.objects.create(user=request.user, what_to_do=what_to, when_to_do=when_to)
        messages.success(request, 'Added')
        return redirect('/my-todolist')


def change_password(request):
    if request.method == 'POST':
        user = request.user
        user = User.objects.get(username=user)
        old_password = request.POST['old_password']
        user = authenticate(request, username=user, password=old_password)
        if user:
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.save()
            return redirect('/logout')
        else:
            message = "Incorrect Password Given"
            form = ChangePasswordForm()
            context = {'message': message, 'form': form}
            return render(request, 'password_change.html', context)
    else:
        form = ChangePasswordForm()
        context = {'form': form}
        return render(request, 'password_change.html', context)
