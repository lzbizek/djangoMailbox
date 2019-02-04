# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from .models import Blog, Category
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    return render_to_response('index.html', {
        'categories': Category.objects.all(),
        'posts': Blog.objects.all(),
		'last10': Blog.objects.all().order_by('-id')[:10]
    })

def view_post(request, id):   
    return render_to_response('view_post.html', {
        'post': get_object_or_404(Blog, id=id)
    })

def view_category(request, id):
    category = get_object_or_404(Category, id=id)
    return render_to_response('view_category.html', {
        'category': category,
        'posts': Blog.objects.filter(category=category)
    })
