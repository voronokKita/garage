import markdown2
import random

from django import forms
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from . import util


class SearchForm(forms.Form):
    search_key = forms.CharField(
        empty_value=None, label="", 
        widget=forms.TextInput(attrs={'placeholder': "search encyclopedia"})
    )


class EditorForm(forms.Form):
    title = forms.CharField(empty_value=None, label="Page name:")
    textarea = forms.CharField(
        empty_value=None, label="Write your article:",
        widget=forms.Textarea
    )


def index(request):
    if request.method == 'GET':
        entries = [entry.capitalize() for entry in util.list_entries()]
        return render(request, "wiki/index.html", {'form': SearchForm(), 'entries': entries})
    
    elif request.method == 'POST':
        keyword = "None"
        entries = util.list_entries()
        form = SearchForm(request.POST)        
        if form.is_valid():
            search_key = form.cleaned_data['search_key'].strip().lower()
            if search_key in entries:
                return HttpResponseRedirect(reverse("wiki:entry", args=(search_key,)))
            else:
                keyword = search_key
        
        return HttpResponseRedirect(reverse("wiki:results", args=(keyword,)))


def entry(request, title):
    title = str(title).strip().lower()
    if title == "random":
        title = random.choice(util.list_entries())
    html_text = markdown2.markdown(
        util.get_entry(title)
    )
    return render(
        request, "wiki/entry.html", 
        {'title': title, 'form': SearchForm(), 'html_text': html_text}
    )


def results(request, keyword):
    entries = []
    if keyword != "None":
        entries = [
            entry.capitalize() for entry in util.list_entries() if keyword in entry
        ]
    return render(request, "wiki/results.html", {'form': SearchForm(), 'entries': entries})


def write(request, entry=None):
    if request.method == 'GET':
        if not entry or entry == "new":
            context = {'form': SearchForm(), 'page_name': "New Page", 
                       'editor_form': EditorForm()}
        else:
            entry = entry.strip().lower()
            if entry not in util.list_entries():
                raise Http404("Article does not exist.")

            text = util.get_entry(entry)
            context = {
                'form': SearchForm(), 'page_name': entry, 
                'editor_form': EditorForm(initial={'title': entry, 'textarea': text})
            }

        return render(request, "wiki/write.html", context)

    elif request.method == 'POST':
        form = EditorForm(request.POST)        
        if not form.is_valid():
            s = "Error: the form is filled out incorrectly."
        else:
            title = form.cleaned_data['title'].strip().lower()
            textarea = form.cleaned_data['textarea']
            util.save_entry(title, textarea)
            s = "Article updated." if title in util.list_entries() else "Article saved."           
            
        context = {'form': SearchForm(), 'editor_form': form, 'page_name': "New Page", 'message': s}
        return render(request, "wiki/write.html", context)    
