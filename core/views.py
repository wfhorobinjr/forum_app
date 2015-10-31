from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import*

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

class ThreadDeleteView(DeleteView):
  model = Thread
  template_name = 'thread/thread_confirm_delete.html'
  success_url = reverse_lazy('thread_list')

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

  def get_success_url(self):
    return self.object.thread.get_absolute_url()

class CommentDeleteView(DeleteView):
  model = Comment
  pk_url_kwarg = 'comment_pk'
  template_name = 'comment/comment_confirm_delete.html'

  def get_success_url(self):
    return self.object.thread.get_absolute_url()