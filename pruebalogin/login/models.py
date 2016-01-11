from django.db import models
from datetime import datetime
from django.contrib import admin

class Noticia(models.Model):
	title = models.CharField(max_length=100, blank = False)
	description = models.TextField(max_length=10000, blank = False)
	date = models.DateField(blank=False, default=datetime.now)
	
	def __unicode__(self):
		return self.title

admin.site.register(Noticia)