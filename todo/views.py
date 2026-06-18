from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

from todo.models import Task


def index(request):
    if request.method == 'POST':
        task = Task(title=request.POST['title'],
                    due_at=make_aware(parse_datetime(request.POST['due_at'])))
        task.save()

    tasks = Task.objects.all()

    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)
