from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseNotAllowed
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.utils.timezone import make_aware

from todo.models import Task


def index(request):
    if request.method == 'POST':
        task = Task(title=request.POST['title'],
                    due_at=make_aware(parse_datetime(request.POST['due_at'])))
        task.save()

    tasks = Task.objects.all()
    status = request.GET.get('status', 'all')
    query = request.GET.get('q', '').strip()

    if status == 'incomplete':
        tasks = tasks.filter(completed=False)
    elif status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'overdue':
        tasks = tasks.filter(completed=False, due_at__lt=timezone.now())

    if query:
        tasks = tasks.filter(title__icontains=query)

    if request.GET.get('order') == 'due':
        tasks = tasks.order_by('due_at')
    else:
        tasks = tasks.order_by('-posted_at')

    blank_task_count = Task.objects.filter(title='').count()

    context = {
        'tasks': tasks,
        'status': status,
        'query': query,
        'order': request.GET.get('order', 'post'),
        'blank_task_count': blank_task_count,
    }
    return render(request, 'todo/index.html', context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)


def react(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        reaction = request.POST.get('reaction')
        if reaction in {'like', 'love', 'wow'}:
            setattr(task, f'{reaction}_count', getattr(task, f'{reaction}_count') + 1)
            task.save(update_fields=[f'{reaction}_count'])

    return redirect(index)


def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect(index)


def delete_blank(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    Task.objects.filter(title='').delete()
    return redirect(index)
  
def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        task.title = request.POST['title']
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect('detail', task.id)

    context = {
        'task': task,
    }
    return render(request, 'todo/edit.html', context)
def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect(index)
