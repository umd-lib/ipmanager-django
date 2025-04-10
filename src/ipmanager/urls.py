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
from django.http import HttpRequest
from django.urls import include, path
from ipmanager.api.views import CheckView, GroupKeyView, GroupsView
from ipmanager.ui.views import (RootView)
from djangosaml2.views import AssertionConsumerServiceView, LogoutInitView

urlpatterns = [
    path('', RootView.as_view(), name='site_root'),
    # SAML
    # --- For the following 2 SAML routes, we are adding them
    # manually because the existing DIT SAML setup is not configured
    # to use the routes that djangosaml2 adds by default. These will
    # override the routes included by djangosaml2.urls
    path('users/auth/saml/callback',
         AssertionConsumerServiceView.as_view(), name="saml2_acs"),
    path('users/auth/saml/slo', LogoutInitView.as_view(), name='saml2_logout'),
    path('saml2/', include('djangosaml2.urls')),
    # Admin
    path('django-admin', admin.site.urls),
    # API
    path('groups/', GroupsView.as_view(), name='groups'),
    path('groups/<group_key>', GroupKeyView.as_view(), name='group_key'),
    path('check', CheckView.as_view(), name='check'),
    # UI
    path("admin/", include('ipmanager.ui.urls'))
]

def get_navigation_links(request: HttpRequest):
    if request.user.is_authenticated:
        return {
            'admin:index': 'Admin',
            '': f'Logged in as {request.user.username}',
            'saml2_logout': 'Log Out',
        }
    else:
        return {
            'saml2_login': 'Log In'
        }