from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from .models import*
from django.core.exceptions import PermissionDenied
from .forms import *

# Create your views here.

class Home(TemplateView):
  template_name = "home.html"

class ThreadCreateView(CreateView):
  model = Thread
  template_name = "thread/thread_form.html"
  fields = ['title', 'link', 'text']
  success_url = reverse_lazy('thread_list')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(ThreadCreateView, self).form_valid(form)

class ThreadListView(ListView):
  model = Thread
  template_name = "thread/thread_list.html"

class ThreadDetailView(DetailView):
  model = Thread
  template_name = 'thread/thread_detail.html'

  def get_context_data(self, **kwargs):
    context = super(ThreadDetailView, self).get_context_data(**kwargs)
    thread = Thread.objects.get(id=self.kwargs['pk'])
    comments = Comment.objects.filter(thread=thread)
    context['comments'] = comments
    return context

class ThreadUpdateView(UpdateView):
  model = Thread
  template_name = 'thread/thread_form.html'
  fields = ['title', 'link', 'text']

  def get_object(self, *args, **kwargs):
    object = super(ThreadUpdateView, self).get_object(*args, **kwargs)
    if object.user != self.request.user:
      raise PermissionDenied()
    return object


class ThreadDeleteView(DeleteView):
  model = Thread
  template_name = 'thread/thread_confirm_delete.html'
  success_url = reverse_lazy('thread_list')

  def get_object(self, *args, **kwargs):
    object = super(ThreadUpdateView, self).get_object(*args, **kwargs)
    if object.user != self.request.user:
      raise PermissionDenied()
    return object


class CommentCreateView(CreateView):
  model = Comment
  template_name = "comment/comment_form.html"
  fields = ['response']

  def get_success_url(self):
    return self.object.thread.get_absolute_url()

  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.thread = Thread.objects.get(id=self.kwargs['pk'])
    return super(CommentCreateView, self).form_valid(form)

class CommentUpdateView(UpdateView):
  model = Comment
  pk_url_kwarg = 'comment_pk'
  template_name = 'comment/comment_form.html'
  fields = ['response']

  def get_object(self, *args, **kwargs):
    object = super(CommentUpdateView, self).get_object(*args, **kwargs)
    if object.user != self.request.user:
      raise PermissionDenied()
    return object

  def get_success_url(self):
    return self.object.thread.get_absolute_url()

class CommentDeleteView(DeleteView):
  model = Comment
  pk_url_kwarg = 'comment_pk'
  template_name = 'comment/comment_confirm_delete.html'

  def get_success_url(self):
    return self.object.thread.get_absolute_url()

  def get_object(self, *args, **kwargs):
    object = super(CommentDeleteView, self).get_object(*args, **kwargs)
    if object.user != self.request.user:
      raise PermissionDenied()
    return object

class VoteFormView(FormView):
  form_class = VoteForm

  def form_valid(self, form):
    user = self.request.user
    thread = Thread.objects.get(pk=form.data['thread'])
    try:
      comment = Comment.objects.get(pk=form.data["comment"])
      prev_votes = Vote.objects.filter(user=user, comment=comment)
      has_voted = (prev_votes.count()>0)
      if not has_voted:
        Vote.objects.create(user=user, comment=comment)
      else:
        prev_votes[0].delete()
      return redirect(reverse('thread_detail', args=[form.data["thread"]]))
    except:
      prev_votes = Vote.objects.filter(user=user, thread=thread)
      has_voted = (prev_votes.count()>0)
      if not has_voted:
        Vote.objects.create(user=user, thread=thread)
      else:
        prev_votes[0].delete()
    return redirect('thread_list')

class UserDetailView(DetailView):
  model = User
  slug_field = 'username'
  template_name = 'user/user_detail.html'
  context_object_name = 'user_in_view'

  def get_context_data(self, **kwargs):
    context = super(UserDetailView, self).get_context_data(**kwargs)
    user_in_view = User.objects.get(username=self.kwargs['slug'])
    threads = Thread.objects.filter(user=user_in_view)
    context['threads'] = threads
    comments = Comment.objects.filter(user=user_in_view)
    context['comments'] = comments
    return context

class UserUpdateView(UpdateView):
  model = User
  slug_field = "username"
  template_name = "user/user_form.html"
  fields = ['email', 'first_name', 'last_name']

  def get_success_url(self):
    return reverse('user_detail', args=[self.request.user.username])

  def get_object(self, *args, **kwargs):
    object = super(UserUpdateView, self).get_object(*args, **kwargs)
    if object != self.request.user:
      raise PermissionDenied()
    return object

class UserDeleteView(DeleteView):
  model = User
  slug_field = "username"
  template_name = "user/user_confirm_delete.html"

  def get_success_url(self):
    return reverse_lazy('logout')

  def get_object(self, *args, **kwargs):
    object = super(UserDeleteView, self).get_object(*args, **kwargs)
    if object != self.request.user:
      raise PermissionDenied()
    return object

  def delete(self, request, *args, **kwargs):
    user = super(UserDeleteView, self).get_object(*args)
    user.is_active = False
    user.save()
    return redirect(self.get_success_url())

class SearchThreadListView(ThreadListView):
  def get_queryset(self):
    incoming_query_string = self.request.GET.get('query', '')
    return Thread.objects.filter(title__icontains=incoming_query_string)