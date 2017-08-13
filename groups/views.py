from braces.views import PrefetchRelatedMixin
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.conf import settings
from . import models

# Create your views here.
class GroupListView(PrefetchRelatedMixin, ListView):
    prefetch_related = ('groupmember_set',)
    model = models.Group
    context_object_name = 'groups'
    ordering = ['group_name']
    paginate_by = 10
    def get_context_data(self):
        context = super().get_context_data()
        context['church_name'] = settings.CHURCH_NAME
        return context


class GroupCreateView(LoginRequiredMixin, CreateView):
    fields = ('group_name', 'group_type', 'group_description')
    template_name = 'groups/group_form.html'
    success_url = reverse_lazy('groups:group_list')
    model = models.Group


class GroupDetailView(PrefetchRelatedMixin, DetailView):
    prefetch_related = ('groupmember_set',)
    model = models.Group
    template_name = 'groups/group_detail.html'


class GroupDeleteView(DeleteView):
    model = models.Group
    success_url = reverse_lazy('groups:group_list')

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects.all()


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Group
    fields = ('group_name', 'group_type', 'group_description')


class GroupSearchView(PrefetchRelatedMixin, ListView):
    prefetch_related = ('groupmember_set', )
    template_name = 'groups/group_list.html'
    model = models.Group
    context_object_name = 'groups'

    def get_queryset(self):
        term = self.request.GET.get('q')
        return self.model.objects.filter(Q(group_name__icontains=term)|Q(group_description__icontains=term)|Q(group_type__group_type__icontains=term)).distinct()


class GroupTypeListView(PrefetchRelatedMixin, ListView):
    prefetch_related = ('group_set',)
    model = models.GroupType
    context_object_name = 'grouptypes'
    ordering = ['group_type']
    paginate_by = 10
    def get_context_data(self):
        context = super().get_context_data()
        context['church_name'] = settings.CHURCH_NAME
        return context


class GroupTypeCreateView(LoginRequiredMixin, CreateView):
    fields = ('group_type')
    template_name = 'groups/grouptype_form.html'
    success_url = reverse_lazy('groups:grouptype_list')
    model = models.GroupType


class GroupTypeDetailView(PrefetchRelatedMixin, DetailView):
    prefetch_related = ('group_set',)
    model = models.GroupType
    template_name = 'groups/grouptype_detail.html'


class GroupTypeDetailView(DetailView, SingleObjectMixin):
    context_object_name = 'group_type'
    template_name = 'families/grouptype_detail.html'


class GroupTypeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'families/grouptype_form.html' 
    model = models.GroupType
    fields = ('group_type')


