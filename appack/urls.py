"""build URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from . import views
from strategy.response import views as vs
from django.conf.urls import url
app_name = 'appack'
admin.autodiscover()

urlpatterns = [
    url(r'^$', vs.get_package, name='getpackage'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^gps/$', views.gps, name='gps'),
    url(r'^packageconfig/', views.packageconfig_view,name='packageconfig'),
    url(r'^sapiloader/', views.sapiloader_view,name='sapiloader'),
    url(r'^sapiloader_add/', views.sapiloader_add_view, name='sapiloader_add'),

    url(r'^sapiloader_c/', views.sapiloader_c_view,name='sapiloader_c'),
    url(r'^sapiloader_c_build/', views.sapiloader_c_build_view,name='sapiloader_c_build'),

    url(r'^superdcf/', views.superdcf_view,name='superdcf'),
    url(r'^zdpi_sig/', views.zdpi_sig_view,name='zdpi_sig'),
    url(r'^superctl/', views.superctl_view,name='superctl'),
    url(r'^dev_model/', views.dev_model_view,name='dev_model'),
    url(r'^packageconfig_add/', views.packageconfig_add_view,name='packageconfig_add'),
    url(r'^dev_model_add/', views.dev_model_add_view,name='dev_model_add'),
    url(r'^superctl_add/', views.superctl_add_view,name='superctl_add'),
    url(r'^superdcf_add/', views.superdcf_add_view,name='superdcf_add'),
    url(r'^superd/$', views.superd_view, name='superd'),
    url(r'^superd_test/$', views.superd_test_view, name='superd_test'),
    url(r'^superd_build/$', views.superd_build_view, name='superd_build'),
    url(r'^superd_build_test/$', views.superd_build_test_view, name='superd_build_test'),
    url(r'^supertack_add/$', views.supertack_add_view, name='supertack_add'),
    url(r'^package/$', views.package_view, name='package'),
    url(r'^release/$', views.release_view, name='release'),
    url(r'^management/$', views.management, name='management'),
    url(r'^oem/', views.oem_view, name='oem'),
    url(r'^oem_add/', views.oem_add_view, name='oem_add'),
    url(r'^tag_add/', views.tag_add_view, name='tag_add'),
    url(r'^advertising/', views.advertising_view, name='advertising'),
    url(r'^connector/', views.connector_view, name='connector'),
    url(r'^auth/', views.auth_view, name='auth'),

]
