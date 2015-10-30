from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.

class Thread(models.Model):
  title = models.CharField(max_length=400)
  link = models.CharField(max_length=300, null=True, blank=True)
  text = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User)

  def get_absolute_url(self):
    return reverse("thread_detail", args=[self.id])

  def __unicode__(self):
    return self.title