from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import task
from .forms import taskform,progressform
from django.contrib.auth.models import User
from .critical_path import main as critical_path_main,calculate_earliest_start,calculate_latest_start,calculate_total_float,calculate_free_float

@login_required(login_url='user-login')
def critical_path_view(request):
    critical_path_main()
    earliest_start = calculate_earliest_start()
    latest_start = calculate_latest_start(earliest_start)
    total_float = calculate_total_float(earliest_start, latest_start)
    free_float = calculate_free_float(earliest_start)

    context = {
        'earliest_start': earliest_start,
        'latest_start': latest_start,
        'total_float': total_float,
        'free_float': free_float,
    }
    return render(request, 'Dashboard/critical_path.html', context)

@login_required(login_url='user-login')
def tasks_view(request):
    items = task.objects.all()
    Tasks_count = items.count()
    Progress_count = items.count()
    users_count = User.objects.all().count()
    
    # Initialize dictionaries
    earliest_start_dict = calculate_earliest_start()
    latest_start_dict = calculate_latest_start(earliest_start_dict)
    total_float_dict = calculate_total_float(earliest_start_dict, latest_start_dict)
    free_float_dict = calculate_free_float(earliest_start_dict)
    
    # Assign calculated values to item attributes
    for item in items:
        item.EarliestST = earliest_start_dict.get(item.Attribute, '')
        item.LatestST = latest_start_dict.get(item.Attribute, '')
        item.tfloat = total_float_dict.get(item.Attribute, '')
        item.ffloat = free_float_dict.get(item.Attribute, '')

    if request.method == 'POST':
        form = taskform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Dashboard-tasks')
    else:
        form = taskform()
    
    context = {
        'items': items,
        'form': form,
        'users_count': users_count,
        'Progress_count': Progress_count,
        'Tasks_count': Tasks_count,
    }
    return render(request, 'Dashboard/tasks.html', context)

@login_required(login_url='user-login')
def index_view(request):
    tasks = task.objects.filter(Staffid=request.user.id)
    return render(request, 'Dashboard/index.html', {'tasks': tasks})


@login_required(login_url='user-login')
def staff_view(request):
    users = User.objects.all()
    users_count = users.count()
    Tasks_count=task.objects.all().count()
    Progress_count=task.objects.all().count()
    tasks = task.objects.all()
    user_tasks = [(user, tasks.filter(Staffid=user.id)) for user in users]
    
    context = {
        'user_tasks': user_tasks,
        'users_count':users_count,
        'Progress_count':Progress_count,
        'Tasks_count':Tasks_count,
    }
    return render(request, 'Dashboard/staff.html', context)

@login_required(login_url='user-login')
def staff_detail(request,pk):
    workers = User.objects.get(id=pk)
    context={
        'workers':workers,
    }
    return render(request,'Dashboard/staff_detail.html',context)



@login_required(login_url='user-login')
def task_delete(request,pk):
    item=task.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('Dashboard-tasks')
    return render(request,'Dashboard/task_delete.html')

@login_required(login_url='user-login')
def task_update(request,pk):
    item=task.objects.get(id=pk)
    if request.method=='POST':
        form=taskform(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('Dashboard-tasks')
    else:
        form=taskform(instance=item)
    context={
        'form':form,
    }
    return render(request,'Dashboard/task_update.html',context)

    

@login_required(login_url='user-login')
def progress_view(request):
    items=task.objects.all()
    Progress_count = items.count()
    Tasks_count=task.objects.all().count()
    users_count = User.objects.all().count()
    if request.method=='POST':
        form1 = progressform(request.POST)
        if form1.is_valid():
            task_id = request.POST.get('task_id')
            item = task.objects.get(id=task_id)
            if item.Progress != 'Done':  # Prevent changes if status is 'done'
                item.Progress = form1.cleaned_data['Progress']
                item.save()
            return redirect(progress_view)
    context = {
        'items': items,
        'form1' : progressform(),
        'users_count':users_count,
        'Progress_count':Progress_count,
        'Tasks_count':Tasks_count,
    }
    return render(request, 'Dashboard/progress.html',context)