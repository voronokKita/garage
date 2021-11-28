from django.shortcuts import render
from django.views.generic.base import TemplateView


def index(request):
    return render(request, "hello/index.html", {'name':"my first Django project"})


def name(request, name):
    return render(request, "hello/index.html", {'name':name.capitalize()})
