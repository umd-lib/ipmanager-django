# Create your views here.
from django.views import View
from django.shortcuts import render
from django.views.generic import ListView
from ipmanager.api.models import Group

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