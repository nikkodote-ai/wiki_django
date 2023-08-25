from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

from . import util

import markdown2 as md

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    get_title = util.get_entry(title)
    if get_title is None:
        return render(request, "encyclopedia/error.html")
    
    else:
        content= md.markdown(get_title)
        return render(request, "encyclopedia/title.html", {
        'title' : title,
        'content' : content
    })
    

def search(request):
    if request.method == 'POST':
        search_word= request.POST['q']
        close_words = []
        print(util.get_entry(search_word))
        if util.get_entry(search_word) is None:
            for word in util.list_entries():
                if search_word.lower() in word.lower():
                    close_words.append(word)
            return render(request, "encyclopedia/index.html", {"entries": close_words})

        else: 
            return HttpResponseRedirect(reverse('title', kwargs = {'title': search_word} ))
    return render(request, "encyclopedia/index.html")

def new_entry(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = f"#{title}\n" + r'{}'.format(request.POST['entry'])

        already_entered = []
        for word in util.list_entries():
            if title.lower() == word.lower():
                already_entered.append(word)
        if len(already_entered) > 0:
            return render(request, "encyclopedia/entry_error.html", {'title': title})
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('title', kwargs = {'title':title}))

    return render(request, 'encyclopedia/new_page.html')

def edit_entry(request, title):
    if request.method == 'POST':
        content = request.POST['entry']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('title', kwargs = {'title':title}))

    content = util.get_entry(title)
    return render(request, 'encyclopedia/edit_page.html', {
        'title': title,
        'content': content
    })

def random_page(request):
    random_word = random.choice(util.list_entries())
    print(random_word)
    return HttpResponseRedirect(reverse('title', kwargs = {'title': random_word} ))