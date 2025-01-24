# Create your views here.
from django.views import View
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from ipmanager.api.models import Group, IPRange, Relation
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse
from ipmanager.ui.forms import IPRangeForm, RelationForm


class HomeView(View):
  def get(self, request):
    return render(request, "ui/index.html", {})

class GroupListView(ListView):
  model = Group
  template_name = 'ui/group_list_view.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'All Groups'
    return context

class SingleGroupView(DetailView):
  model = Group
  template_name = 'ui/single_group_view.html'
  
  slug_field = 'key'
  slug_url_kwarg = 'key'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    current_group = self.object

    context.update(
      relation_form=RelationForm(initial={'subject' : self.object}),
      ip_ranges=IPRange.objects.filter(group=current_group),
      included_groups=Relation.objects.filter(subject=current_group, relation=Relation.RelationType.INCLUSION),
      excluded_groups=Relation.objects.filter(subject=current_group, relation=Relation.RelationType.EXCLUSION),
      ip_range_form = IPRangeForm(initial={'group': current_group}), 
    )

    return context

class EditGroupView(UpdateView):
 model = Group
 fields = ['key', 'name', 'description', 'notes', 'export']
 template_name = 'ui/edit_group.html'

 def get_success_url(self):
   return reverse('single_group', args=[self.object.key])
 
 def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    current_group = Group.objects.filter(pk=self.object.pk).first()
    context.update(
      group = current_group
    )
    return context

class CreateGroupView(CreateView):
  model = Group
  fields = ['key', 'name', 'description', 'notes', 'export']
  template_name = 'ui/new_group.html'
  def get_success_url(self):
    return reverse('single_group', args=[self.object.key])

class DeleteGroupView(DeleteView):
  model = Group

  def get_success_url(self):
    return reverse('list_all_groups')

class CreateRelationView(CreateView):
  form_class = RelationForm
  template_name = 'ui/create_relation_form.html'
  def get_success_url(self):
    return reverse('single_group', args=[self.object.subject.key])

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update(
      group = Group.objects.filter(key=self.kwargs.get('key')).first()
    )
    return context
  
class DeleteRelationView(DeleteView):
  model = Relation

  def get_success_url(self):
    return reverse('single_group', args=[self.object.subject.key])

class CreateIPRangeView(CreateView):
  form_class = IPRangeForm
  template_name = 'ui/add_ip_range_form.html'
  def get_success_url(self):
    return reverse('single_group', args=[self.object.group.key])
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    current_group = Group.objects.filter(key=self.kwargs.get('key')).first()
    context.update(
      group = current_group
    )
    return context
  
class DeleteIPRangeView(DeleteView):
  model = IPRange
  def get_success_url(self):
    return reverse('single_group', args=[self.object.group.key])