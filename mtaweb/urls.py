from django.conf.urls import  url
from django.views.generic import TemplateView

import mtaweb.views as views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^introduction/$', views.introduction, name='introduction'),
    url(r'^download/$', views.download, name='download'),
    # url(r'^download/(?P<filter_by>[a-zA_Z]+)/$', views.download, name='download')
]

