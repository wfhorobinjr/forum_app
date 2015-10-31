from django.conf.urls import patterns, include, url
from .views import*
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
  url(r'^$', Home.as_view(), name='home'),
  url(r'^user/', include('registration.backends.simple.urls')),
  url(r'^user/', include('django.contrib.auth.urls')),
  url(r'^thread/create/$', login_required(ThreadCreateView.as_view()), name='thread_create'),
  url(r'^thread/$', login_required(ThreadListView.as_view()), name='thread_list'),
  url(r'^thread/(?P<pk>\d+)/$', login_required(ThreadDetailView.as_view()), name='thread_detail'),
  url(r'^thread/update/(?P<pk>\d+)/$', login_required(ThreadUpdateView.as_view()), name='thread_update'),
  url(r'^thread/delete/(?P<pk>\d+)/$', login_required(ThreadDeleteView.as_view()), name='thread_delete'),
  url(r'^thread/(?P<pk>\d+)/comment/create/$', login_required(CommentCreateView.as_view()), name='comment_create'),
  url(r'^thread/(?P<thread_pk>\d+)/comment/update/(?P<comment_pk>\d+)/$', login_required(CommentUpdateView.as_view()), name='comment_update'),
  url(r'^thread/(?P<thread_pk>\d+)/comment/delete/(?P<comment_pk>\d+)/$', login_required(CommentDeleteView.as_view()), name='comment_delete'),
  url(r'^vote/$', login_required(VoteFormView.as_view()), name='vote'),
  url(r'^user/(?P<slug>\w+)/$', login_required(UserDetailView.as_view()), name='user_detail'),
)
