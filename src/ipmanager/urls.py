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
from django.urls import include, path

from ipmanager.api.views import CheckView, GroupKeyView, GroupsView
from ipmanager.ui.views import (CreateGroupView, CreateIPRangeView, CreateRelationView, DeleteGroupView,
                                DeleteIPRangeView, DeleteRelationView, EditGroupView, GroupListView, HomeView, RootView,
                                SingleGroupView)

urlpatterns = [
    path('', RootView.as_view(), name='site_root'),
    path('saml2/', include('djangosaml2.urls')),
    path('home', HomeView.as_view(), name='home_page'),
    path('django-admin', admin.site.urls),
    path('groups', GroupsView.as_view(), name='groups'),
    path('admin/groups', GroupListView.as_view(), name='list_all_groups'),
    path('check', CheckView.as_view(), name='check'),
    path('groups/<group_key>', GroupKeyView.as_view(), name='group_key'),
    path('admin/groups/<str:key>', SingleGroupView.as_view(), name='single_group'),
    path('admin/groups/<int:pk>/edit', EditGroupView.as_view(), name='edit_group'),
    path('admin/groups/create', CreateGroupView.as_view(), name='create_group'),
    path(
        'admin/groups/<int:pk>/delete', DeleteGroupView.as_view(), name='delete_group'
    ),
    path(
        'admin/groups/<str:key>/relation/create',
        CreateRelationView.as_view(),
        name='relation',
    ),
    path(
        'admin/groups/<str:key>/relation/<int:pk>/delete',
        DeleteRelationView.as_view(),
        name='delete_relation',
    ),
    path(
        'admin/groups/<str:key>/ip_ranges',
        CreateIPRangeView.as_view(),
        name='create_new_ip_range',
    ),
    path(
        'admin/groups/<str:key>/ip_ranges/<int:pk>/delete',
        DeleteIPRangeView.as_view(),
        name='delete_ip_range',
    ),
]
