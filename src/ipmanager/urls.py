"""
URL configuration for ipmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from ipmanager.api.views import GroupsView, GroupKeyView, CheckView
from ipmanager.ui.views import HomeView, GroupListView, SingleGroupView, EditGroupView

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home_page"),
    path('groups/', GroupsView.as_view(), name="groups"),
    path('admin/groups', GroupListView.as_view(), name="list_all_groups"),
    path("check", CheckView.as_view(), name="check"),
    path('groups/<group_key>/', GroupKeyView.as_view(), name="group_key"),
    path('admin/groups/<str:key>/', SingleGroupView.as_view(), name="single_group"),
    path('admin/groups/<int:pk>/edit', EditGroupView.as_view(), name="edit_group"),
]