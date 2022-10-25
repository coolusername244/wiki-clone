from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown

from . import util

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    content = util.get_entry(entry)

    if content is not None:
        return render(request, "encyclopedia/content.html", {
            "content": markdowner.convert(content)
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