from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ipmanager.api.models import Group, IPRange, Relation
from ipmanager.ui.forms import IPRangeForm, RelationForm, TestIPForm

class RootView(TemplateView):
    template_name = 'ui/login_required.html'

    def get(self, request, *args, **kwargs):
        """If the user is already logged in, send them to the home page.
        Otherwise, display the "Login Required" page."""

        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('list_all_groups'))
        else:
            return super().get(request, *args, **kwargs)

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'ui/index.html', {})

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'ui/group_list_view.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        test_ip = self.request.GET.get('test_ip', '')
        if test_ip:
            for group in queryset:
                group.contained = test_ip in group
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Groups'
        context.update(
            form=TestIPForm,
            test_ip=self.request.GET.get('test_ip', ''),
        )
        return context


class SingleGroupView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'ui/single_group_view.html'

    slug_field = 'key'
    slug_url_kwarg = 'key'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_group = self.object

        test_ip = self.request.GET.get('test_ip', '')
        contained = None
        if test_ip:
            contained = test_ip in current_group

        context.update(
            relation_form=RelationForm(initial={'subject': self.object}),
            ip_ranges=IPRange.objects.filter(group=current_group),
            included_groups=Relation.objects.filter(
                subject=current_group, relation=Relation.RelationType.INCLUSION
            ),
            excluded_groups=Relation.objects.filter(
                subject=current_group, relation=Relation.RelationType.EXCLUSION
            ),
            ip_range_form=IPRangeForm(initial={'group': current_group}),
            form=TestIPForm,
            contained=contained,
            test_ip=test_ip,
        )

        return context


class EditGroupView(LoginRequiredMixin, UpdateView):
    model = Group
    fields = ['key', 'name', 'description', 'notes', 'export']
    template_name = 'ui/edit_group.html'

    def get_success_url(self):
        return reverse('single_group', args=[self.object.key])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_group = Group.objects.filter(pk=self.object.pk).first()
        context.update(group=current_group)
        return context


class CreateGroupView(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['key', 'name', 'description', 'notes', 'export']
    template_name = 'ui/new_group.html'

    def get_success_url(self):
        return reverse('single_group', args=[self.object.key])


class DeleteGroupView(LoginRequiredMixin, DeleteView):
    model = Group

    def get_success_url(self):
        return reverse('list_all_groups')


class CreateRelationView(LoginRequiredMixin, CreateView):
    form_class = RelationForm
    template_name = 'ui/create_relation_form.html'

    def get_success_url(self):
        return reverse('single_group', args=[self.object.subject.key])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(group=Group.objects.filter(key=self.kwargs.get('key')).first())
        return context


class DeleteRelationView(LoginRequiredMixin, DeleteView):
    model = Relation

    def get_success_url(self):
        return reverse('single_group', args=[self.object.subject.key])


class CreateIPRangeView(LoginRequiredMixin, CreateView):
    form_class = IPRangeForm
    template_name = 'ui/add_ip_range_form.html'

    def get_success_url(self):
        return reverse('single_group', args=[self.object.group.key])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_group = Group.objects.filter(key=self.kwargs.get('key')).first()
        context.update(group=current_group)
        return context


class DeleteIPRangeView(LoginRequiredMixin, DeleteView):
    model = IPRange

    def get_success_url(self):
        return reverse('single_group', args=[self.object.group.key])
