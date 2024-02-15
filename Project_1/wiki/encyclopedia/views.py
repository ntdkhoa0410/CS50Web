from django.shortcuts import render
from . import util
from django.http import HttpResponse
from markdown2 import Markdown
import random

def convert_Md_to_HTML(title):
    md_content = util.get_entry(title)
    markdown_md = Markdown()
    if md_content == None:
        return "no data for this entry"
    else:
        return markdown_md.convert(md_content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_page(request, name):
    data = convert_Md_to_HTML(name)
    return render(request, "encyclopedia/entry.html", {
        "entry": data,
        "name": name
    })

   
def search(request):
    if request.method == "POST":
        search_data = request.POST['q']
        entries = util.list_entries()
        html_data = convert_Md_to_HTML(search_data)
        if html_data is not "no data for this entry":
            return render(request, "encyclopedia/entry.html", {
            "entry": html_data,
            "name": search_data
        })
        else:
            recommendation = []
            for entry in entries:
                if search_data.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "entries": recommendation
            })

def add(request):
    if request.method == "GET":
        return render(request, "encyclopedia/add.html")
    else:
        new_title = request.POST['title']
        new_data = request.POST['content']
        if util.get_entry(new_title) is not None:
            return render(request, "encyclopedia/entry.html", {
                "entry": "this data already exist",
                "name": new_title
        })
        else:
            util.save_entry(new_title, new_data)
            content = convert_Md_to_HTML(new_title)
            return render(request, "encyclopedia/entry.html", {
                "entry": content,
                "name": new_title
        })
    
def edit(request):
    if request.method == "POST":
        old_title = request.POST['old_title']
        old_content = util.get_entry(old_title)
        #old_content = request.POST['old_entry']
        return render(request, "encyclopedia/edit.html", {
            "title": old_title,
            "content": old_content
        })
    
def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        markdown_md = Markdown()
        real_data = markdown_md.convert(content)
        util.save_entry(title,content)
        return render(request, "encyclopedia/entry.html", {
                "entry": real_data,
                "name": title
        })
    
def random_page(request) : 
    entries = util.list_entries() 
    rand_entry = random.choice(entries) 
    html_content = convert_Md_to_HTML(rand_entry) 
    return render(request, "encyclopedia/entry.html", {
            "entry": html_content,
            "name": rand_entry
    })