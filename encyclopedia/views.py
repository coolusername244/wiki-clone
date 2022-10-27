import random

from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown

from . import util

markdowner = Markdown()

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    content = util.get_entry(entry)

    # checks if content exists in entries folder
    if content:
        return render(request, "encyclopedia/content.html", {
            "content": markdowner.convert(content),
            "entry": entry
        })
    # if user has entered a search via search bar, display "no results found"
    # with user input
    else:
        return render(request, "encyclopedia/search_results.html", {
            "entry": entry
        })

def search(request):
    if request.method == "POST":
        entry = request.POST['q'].lower()
        content = util.get_entry(entry)
        entries = util.list_entries()
        results = []

        # if search yeilds 1 result - go to page
        if content:
            return render(request, "encyclopedia/content.html", {
                "content": markdowner.convert(content)
            })
        
        # if search yeilds many results - list all entries
        for i in entries:
            if entry in i.lower():
                results.append(i)
        return render(request, "encyclopedia/search_results.html", {
            "results": results,
            "entry": entry
        })
       

def create(request):

    if request.method == "POST":
        entries = util.list_entries()
        form = NewEntryForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if title in entries:
                messages.error(request, 'Entry with this name already exists')
                return render(request, "encyclopedia/create.html", {
                    "form": form
                })
            else:
                util.save_entry(title, content)
                return redirect('entry', entry=title)
        # if form is invalid/tampered with, send back to user
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm()
        })

def edit(request, entry):
    content = util.get_entry(entry)

    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("entry", args=[entry]))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })
    else:
        form = EditEntryForm(initial={'content': content})
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "entry": entry
        })


def random_page(request):
    entry = random.choice(util.list_entries())
    return redirect('entry', entry=entry)
