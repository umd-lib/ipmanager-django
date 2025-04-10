from django.urls import path

from .views import (CreateGroupView, CreateIPRangeView, CreateRelationView, DeleteGroupView,
                    DeleteIPRangeView, DeleteRelationView, EditGroupView, GroupListView, RootView,
                    SingleGroupView)

urlpatterns = [
    path('groups', GroupListView.as_view(), name='list_all_groups'),
    path('groups/create',
         CreateGroupView.as_view(), name='create_group'),
    path('groups/<str:key>',
         SingleGroupView.as_view(), name='single_group'),
    path('groups/<int:pk>/edit',
         EditGroupView.as_view(), name='edit_group'),
    path(
        'groups/<int:pk>/delete', DeleteGroupView.as_view(), name='delete_group'
    ),
    path(
        'groups/<str:key>/relation/create',
        CreateRelationView.as_view(),
        name='relation',
    ),
    path(
        'groups/<str:key>/relation/<int:pk>/delete',
        DeleteRelationView.as_view(),
        name='delete_relation',
    ),
    path(
        'groups/<str:key>/ip_ranges',
        CreateIPRangeView.as_view(),
        name='create_new_ip_range',
    ),
    path(
        'groups/<str:key>/ip_ranges/<int:pk>/delete',
        DeleteIPRangeView.as_view(),
        name='delete_ip_range',
    ),
]
