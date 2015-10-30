from django.conf.urls import patterns, include, url
from .views import*

urlpatterns = patterns('',
  url(r'^$', Home.as_view(), name='home'),
  url(r'^user/', include('registration.backends.simple.urls')),
  url(r'^user/', include('django.contrib.auth.urls')),
  url(r'^thread/create/$', ThreadCreateView.as_view(), name='thread_create'),
  url(r'^thread/$', ThreadListView.as_view(), name='thread_list'),
  url(r'^thread/(?P<pk>\d+)/$', ThreadDetailView.as_view(), name='thread_detail'),
)