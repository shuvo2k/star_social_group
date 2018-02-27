#gropus models.py
from django.db import models
from django.utils.text import slugify 
import misaka         #let us use markdown inside post
from django.core.urlresolvers import reverse 

from django import template 
register = template.Library()

from django.contrib.auth import get_user_model
User = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugFiled(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships')
    user = models.ForeignKey(User, related_name='user_group')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')