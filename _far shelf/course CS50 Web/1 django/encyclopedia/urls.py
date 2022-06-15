from django.urls import path
from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:title>", views.entry, name="entry"),
    path("results/<str:keyword>", views.results, name="results"),
    path("write/", views.write, name="write"),
    path("write/<str:entry>", views.write, name="write"),
]
