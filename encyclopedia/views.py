import random

from django import forms
from django.contrib import messages
from django.shortcuts import render
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

    if content is not None:
        return render(request, "encyclopedia/content.html", {
            "content": markdowner.convert(content),
            "entry": entry
        })
    else:
        return render(request, "encyclopedia/noresult.html", {
            "entry": entry
        })

def search(request):
    if request.method == "POST":
        query = request.POST['q'].lower()
        content = util.get_entry(query)
        entries = util.list_entries()
        results = []

        if content is not None:
            return render(request, "encyclopedia/content.html", {
                "content": markdowner.convert(content)
            })
        
        for i in entries:
            if query in i.lower():
                results.append(i)

        if len(results) == 0:
            return render(request, "encyclopedia/search_results.html")
        else:
            return render(request, "encyclopedia/search_results.html", {
                "results": results
            })
            
    else:
        return render(request, "encyclopedia/search_results.html")        

def create(request):

    if request.method == "POST":
        entries = util.list_entries()
        form = NewEntryForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if title in entries:
                print("found return duplicate error")

                messages.error(request, 'Entry with this name already exists')
                return render(request, "encyclopedia/create.html", {
                    "form": form
                })
            else:
                util.save_entry(title, content)
                new_entry = util.get_entry(title)
                return render(request, "encyclopedia/content.html", {
                    "content": markdowner.convert(new_entry)
                })

    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm()
        })

def edit(request, entry):
    content = util.get_entry(entry)
    print(entry)

    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("entry", args=[entry]))

    else:
        form = EditEntryForm(initial={'content': content})
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "entry": entry
        })


def random_page(request):
    n = random.randint(0, (len(util.list_entries()) -1))

    entries = util.list_entries()
    rand_entry = entries[n]
    content = util.get_entry(rand_entry)
    return render(request, "encyclopedia/content.html", {
        "content": markdowner.convert(content),

    })