"""pruebalogin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from login.views import index_view, salir, MuestraNoticia, MuestraTodasNoticias, CreaNoticia, ActualizaNoticia, BorraNoticia

urlpatterns = [
    url(r'^$', index_view),
    url(r'^salir/$', salir),
    url(r'^(?P<pk>\d+)/$', MuestraNoticia.as_view()),
    url(r'list/$', MuestraTodasNoticias.as_view(), name='post-list'),
    url(r'noticia/add/$', CreaNoticia.as_view(), name='author-add'),
    url(r'noticia/(?P<pk>[0-9]+)/$', ActualizaNoticia.as_view(), name='author-update'),
    url(r'noticia/(?P<pk>[0-9]+)/delete/$', BorraNoticia.as_view(), name='author-delete'),
]
