from django.shortcuts import render
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