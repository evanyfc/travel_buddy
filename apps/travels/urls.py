from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^add/$', add, name='add'),
    url(r'^create/$', create, name='create'),
    url(r'^destination/(?P<id>\d+)$', show, name='show'),
    url(r'^join/(?P<id>\d+)$', jointrip, name='jointrip'),
]
