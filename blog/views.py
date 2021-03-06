from django.views import generic
from . import models
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
import os
import mimetypes
from wsgiref.util import FileWrapper
from blog.forms import UserForm, EntryForm, TagForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django import forms
from django.contrib.auth.hashers import make_password
from blog.models import User, Entry, Tag
from django.shortcuts import render
from django.db.models import Sum, Q
import CryptoLib
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import hashlib
import os, tempfile, zipfile
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.contrib import admin

class TagList(ListView):
    model = Tag
    template_name = "tag_list.html"

class TagCreate(CreateView):
    form_class = TagForm
    success_url = reverse_lazy('index')
    template_name = "tag_form.html"    
    
#class TagDetail(generic.DetailView):
 #   model = models.Tag
 #   blogs = Entry.objects.filter( Q(tagline = model)).order_by('-created')
 #   render('tag.html',{'blogs': blogs}) 
    
class EntryCreate(CreateView):
    form_class = EntryForm
    success_url = reverse_lazy('index')
    template_name = "entry_form.html"    
    
class EntryDelete(DeleteView):
    model = Entry
    success_url = reverse_lazy('index')
    template_name = "entry_confirm_delete.html"
    
class UserCreate(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('user_login')
    template_name = "user_form.html"
    
class BlogIndex(generic.ListView):
    queryset = models.Entry.objects.published()
    template_name = "home.html"
    paginate_by = 3

class BlogDetail(generic.DetailView):
    model = models.Entry
    template_name = "post.html"
    
class BlogUpdate(UpdateView):
    model = models.Entry
    form_class = EntryForm
    template_name = "entry_form.html"
    success_url = reverse_lazy('index')

class TagUpdate(UpdateView):
    model = models.Tag
    slug_field = 'name'    
    form_class = TagForm
    template_name = "tag_form.html"
    success_url = reverse_lazy('index')
    
      
class TagDelete(DeleteView):
    model = Tag
    slug_field = 'name'        
    success_url = reverse_lazy('index')
    template_name = "tag_confirm_delete.html"
    
def search_form(request):
    return render(request, 'search_form.html')

def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
	    blogs = Entry.objects.filter( Q(title__icontains = q) | Q(body__icontains = q)).order_by('title')
            return render(request, 'search_results.html',
                {'blogs': blogs, 'query': q})
    return render(request, 'search_form.html',
        {'error': error})

def decrypt_form(request, slug):
    success_url = request.META.get('HTTP_REFERER')
    return render(request, 'decrypt_form.html', {'slug':slug})

def decrypt(request):

    myEntry = Entry.objects.filter(slug=request.GET['slug'])[0]
    fileName = default_storage.path(myEntry.myFile)
    key = hashlib.sha256(request.GET['pass']).digest() 

    try:
        CryptoLib.decrypt_file(key, fileName)
        dec_filePath = default_storage.path(fileName[:-4])

        print dec_filePath

        wrapper = FileWrapper(file(dec_filePath))
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Length'] = os.path.getsize(dec_filePath)

        default_storage.delete(fileName[:-4])

    except:
        #nuke the media directory
        shutil.rmtree(default_storage.path(''))
        os.mkdir(default_storage.path(''))
        raise

    return response
  
def folder_view(request):
    return render(request, 'folder_view.html')
  
def folderview(request):
    if 'q' in request.GET:
        q = request.GET['q']
        folder = Tag.objects.get(name = q)
	blogs = Entry.objects.filter( Q(tagline = folder))
        return render(request, 'tag.html',
            {'blogs': blogs, 'folder': folder})

def copy_blog(blog_slug):
    obj = Entry.objects.get(slug = blog_slug)
    obj.slug = "test"
    obj.save()
    
