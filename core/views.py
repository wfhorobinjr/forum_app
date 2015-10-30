from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
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

class ThreadUpdateView(UpdateView):
  model = Thread
  template_name = 'thread/thread_form.html'
  fields = ['title', 'link', 'text']