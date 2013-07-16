from django.conf.urls import patterns, include, url

from hello import views

urlpatterns = patterns('',	
    (r'^(.*)$', views.hello)
)
