from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.

SUBJECT_CHOICES = (
(0, "Miscellaneous"),
(1, "Clubs and Activities"),
(2, "Nightlife"),
(3, "Athletics"),
(4, "Res Life"),
(5, "Academics"),
)

class Thread(models.Model):
  title = models.CharField(max_length=400)
  link = models.CharField(max_length=300, null=True, blank=True)
  text = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User)
  subject = models.IntegerField(choices=SUBJECT_CHOICES, default=0)

  def get_absolute_url(self):
    return reverse("thread_detail", args=[self.id])

  def __unicode__(self):
    return self.title

class Comment(models.Model):
  thread = models.ForeignKey(Thread)
  user = models.ForeignKey(User)
  created_at = models.DateTimeField(auto_now_add=True)
  response = models.TextField()

  def __unicode__(self):
    return self.response

class Vote(models.Model):
  user = models.ForeignKey(User)
  thread = models.ForeignKey(Thread, blank=True, null=True)
  comment = models.ForeignKey(Comment, blank=True, null=True)

  def __unicode__(self):
    return "%s upvoted" % (self.user.username)