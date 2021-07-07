from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)


def index(request):
    if 'tasks' not in request.session:
        request.session['tasks'] = []
    return render(request, "tasks/index.html", {'tasks': request.session['tasks']})


def add(request):
    if request.method == 'GET':
        return render(request, "tasks/add.html", {'form': NewTaskForm()})
        
    elif request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data['task']
            priority = form.cleaned_data['priority']
            request.session['tasks'] += [f"{priority}. {task}"]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {'form': form})
