import datetime

from django.shortcuts import render


def index(request):
    now = datetime.datetime.now()
    result = now.month == 1 and now.day == 1
    return render(request, "newyear/index.html", {'newyear': result} )
