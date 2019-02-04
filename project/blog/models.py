# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import permalink
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# Create your models here.
class Blog(models.Model):
	author = models.CharField(max_length=100, default="Anonymous")
	title = models.CharField(max_length=200)
	body = models.TextField()
	posted = models.DateField(db_index=True, auto_now_add=True)
	category = models.ForeignKey('blog.Category')

	def __unicode__(self):
		return '%s' % self.title

	@permalink
	def get_absolute_url(self):
		return ('view_blog_post', None, { 'id': self.id })

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    
    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_category', None, { 'id': self.id })
