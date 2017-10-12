from django.conf.urls import url
from . import views

app_name = 'static'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<category_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<file_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^files/(?P<filter_by>[a-zA_Z]+)/$', views.files, name='files'),
    url(r'^create_category/$', views.create_category, name='create_category'),
    url(r'^(?P<category_id>[0-9]+)/create_file/$', views.create_file, name='create_file'),
    url(r'^(?P<category_id>[0-9]+)/delete_file/(?P<file_id>[0-9]+)/$', views.delete_file, name='delete_file'),
    url(r'^(?P<category_id>[0-9]+)/favorite_category/$', views.favorite_category, name='favorite_category'),
    url(r'^(?P<category_id>[0-9]+)/delete_category/$', views.delete_category, name='delete_category'),
]
