# Create your views here.
from django.views import View
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from ipmanager.api.models import Group, IPRange, Relation
from django.views.generic.edit import UpdateView
from django.urls import reverse

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
    ip_ranges=IPRange.objects.filter(group=current_group),
    included_groups=Relation.objects.filter(subject=current_group, relation=Relation.RelationType.INCLUSION),
    excluded_groups=Relation.objects.filter(subject=current_group, relation=Relation.RelationType.EXCLUSION),
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
