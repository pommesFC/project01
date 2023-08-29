from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.urls import reverse
from markdown2 import Markdown
from django import forms
import random

from . import util

class NewForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'id':'title','placeholder':'Enter the Title: ',}))
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'id':'body','placeholder':'Enter the details in Markdown format. Checkout its page to know more about it.'}))

class EditForm(forms.Form):
    edited_content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Edit here:'}))

    def clean_edited_content(self):
        content = self.cleaned_data['edited_content']
        if not content:
            raise forms.ValidationError('Please enter some content.')
        return content


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def display(request, title):
    entry_md = util.get_entry(title)
    if entry_md != None:
        entry_html = Markdown().convert(entry_md)
        return render(request, "encyclopedia/entry.html",{
        "title":title,
        "content":entry_html
    })
    else:
        return render(request, "encyclopedia/none.html",{
    })
def newPage(request):
    form = NewForm()
    if request.method == "GET":
            return render(request, "encyclopedia/newPage.html",{
        "form": NewForm()
    })

    elif request.method == "POST":
        form = NewForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            entries = util.get_entry(title)
            if entries == None:
                util.save_entry(title, body)
                message = "New title has been added successfully!"
                return redirect(reverse('newPage'),{
                    "message": message
                })
            else:
                return render(request, "encyclopedia/error.html")
def randomPage(request):
    titles = util.list_entries()
    random_page = random.choice(titles)
    return redirect(reverse('display', args=[random_page]))

def searchbar(request):
    query = request.GET.get("q")
    return redirect(reverse('display',args=[query]))

def edit(request, titles):
    entry = util.get_entry(titles)
    initial_form = EditForm(initial={'edited_content': entry})

    if not entry:
        messages.error(request, f'{titles} page does not exist and can\'t be edited, please create a new page instead!')
        return redirect('index')

    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data['edited_content']
            util.save_entry(titles, new_content)
            messages.success(request, f'Entry {titles} updated successfully!')
            return redirect(reverse('display', args=[titles]))
        else:
            messages.error(request, f'Editing form not valid, please try again!')
            return render(request, 'encyclopedia/edit.html', {
                'form': initial_form,
                'title': titles
            })

    return render(request, 'encyclopedia/edit.html', {
        'form': initial_form,
        'title': titles
    })
