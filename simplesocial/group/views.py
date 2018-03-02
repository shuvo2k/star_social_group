from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import (LoginRequiredMixin, 
                                        PemissionRequiredMixin)
from django.core.urlresolvers import reverse
from django.views import generic
from group.models import Group, GroupMember
from django.shortcuts import get_object_or_404

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group


class SingleGroup(generic.DetailView):
    model = Group


class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('group:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError: 
            message.warning(self.request, "Warning already a member!!")
        else:
            message.success(self.request, "You are now a member!")
        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('group:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(
                user = self.request.user,
                group__slug=self.kwargs.get('slug')

            ).get()
        except models.GroupMember.DoesNotExist:
            message.warning(self.request, "Sorry you are not in this group!")
        else:
            membership.delete()
            message.success(self.request, "You have left this group!")
        return super().get(request, *args, **kwargs)

    