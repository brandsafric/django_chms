from itertools import chain

from braces.views import PrefetchRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from . import forms
from . import models

# Create your views here.

class FamilyListView(PrefetchRelatedMixin, ListView):
    prefetch_related = ('adult_set', 'child_set')
    model = models.Family
    context_object_name = 'families'
    paginate_by = 10

    def get_context_data(self):
        context = super().get_context_data()
        context['email'] = 'jdoepp@gmail.com'
        return context


class FamilyDetailView(PrefetchRelatedMixin, DetailView):
    prefetch_related = ('adult_set', 'child_set')
    model = models.Family
    template_name = 'families/family_detail.html'


class FamilyCreateView(LoginRequiredMixin, CreateView):
    fields = ('user', 'family_name', 'address1', 'address2', 'city', 'postal_code', 'state', 'country', 'notes')
    model = models.Family
    success_url = reverse_lazy('families:list')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.pk
        return initial


class FamilyDeleteView(DeleteView):
    model = models.Family
    success_url = reverse_lazy('families:list')

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects.all()


class FamilyUpdateView(LoginRequiredMixin, UpdateView):
    fields = ('user', 'family_name', 'address1', 'address2', 'city', 'postal_code', 'state', 'country', 'notes')

    model = models.Family


class FamilySearchView(PrefetchRelatedMixin, ListView):
    prefetch_related = ('adult_set', 'child_set')
    template_name = 'families/family_list.html'
    model = models.Family
    context_object_name = 'families'

    def get_queryset(self):
        term = self.request.GET.get('q')
        return self.model.objects.filter(Q(family_name__icontains=term)|Q(adult__first_name__icontains=term)|Q(child__first_name__icontains=term)).distinct()

    def get_context_data(self):
        context = super().get_context_data()
        context['email'] = 'jdoepp@gmail.com'
        return context


class AdultCreateView(LoginRequiredMixin, CreateView):
    model = models.Adult
    fields = ('title', 'first_name', 'last_name', 'suffix', 'gender', 'birth_date', 'marital_status', 'date_joined', 'occupation', 'workplace', 'work_address','notes')
    template_name = 'families/member_form.html'

    def get_success_url(self):
        return reverse_lazy('families:family_detail', kwargs={'pk': self.kwargs['family_pk']})

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.pk
        initial['last_name'] = models.Family.objects.get(pk=self.kwargs['family_pk']).family_name
        return initial

    def get_context_data(self):
        context = super().get_context_data()
        context['member_type'] = 'a'
        context['family_pk'] = self.kwargs['family_pk']
        return context

    def form_valid(self, form):
        form.instance.family_id = self.kwargs['family_pk']
        return super(AdultCreateView, self).form_valid(form)


class MemberDetailView(DetailView, SingleObjectMixin):
    context_object_name = 'member'
    template_name = 'families/member_detail.html'
    pk_url_kwarg = 'member_pk'

    def get_queryset(self):
        if self.kwargs['member_type'] == 'a':
            return models.Adult.objects.select_related('family').filter(family_id=self.kwargs['family_pk'])
        else:
            return models.Child.objects.select_related('family').filter(family_id=self.kwargs['family_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member_type'] = self.kwargs['member_type']
        context['member_pk'] = self.kwargs['member_pk']
        context['family_pk'] = self.kwargs['family_pk']
        if self.kwargs['member_type'] == 'd':
            context['age'] = self.get_queryset().get(pk=self.kwargs['member_pk']).age()
        else:
            context['age'] = None
        return context


class ChildCreateView(LoginRequiredMixin, CreateView):
    model = models.Child
    fields = ('title', 'first_name', 'last_name', 'suffix', 'gender', 'birth_date', 'date_joined', 'school','notes')
    template_name = 'families/member_form.html'
    #success_url = reverse_lazy('families:family_detail', kwargs={'pk': model.family.pk})

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.pk
        initial['last_name'] = models.Family.objects.get(pk=self.kwargs['family_pk']).family_name
        return initial

    def get_context_data(self):
        context = super().get_context_data()
        context['member_type'] = 'd'
        context['family_pk'] = self.kwargs['family_pk']
        return context

    def form_valid(self, form):
        form.instance.family_id = self.kwargs['family_pk']
        return super(ChildCreateView, self).form_valid(form)


class ChildUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'families/member_form.html' 
    model = models.Child
    fields = ('title', 'first_name', 'last_name', 'suffix', 'gender', 'birth_date', 'date_joined', 'school','notes')
    pk_url_kwarg = 'member_pk'

    #def get_success_url(self):
    #    return reverse_lazy('families:member_detail', kwargs={'family_pk': self.kwargs['family_pk'], 'member_pk': self.kwargs['pk'], 'member_type': 'd'})

    def get_context_data(self):
        context = super().get_context_data()
        context['member_type'] = 'd'
        context['family_pk'] = self.kwargs['family_pk']
        context['member_pk'] = self.kwargs['member_pk']
        return context


class AdultUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'families/member_form.html' 
    model = models.Adult
    fields = ('title', 'first_name', 'last_name', 'suffix', 'gender', 'birth_date', 'marital_status', 'date_joined', 'occupation', 'workplace', 'work_address','notes')
    pk_url_kwarg = 'member_pk'

    def get_success_url(self):
        return reverse_lazy('families:member_detail', kwargs={'family_pk': self.kwargs['family_pk'], 'member_pk': self.kwargs['member_pk'], 'member_type': 'a'})

    def get_context_data(self):
        context = super().get_context_data()
        context['member_type'] = 'a'
        context['family_pk'] = self.kwargs['family_pk']
        context['member_pk'] = self.kwargs['member_pk']
        return context

