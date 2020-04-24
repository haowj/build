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
from django.conf.urls import url
app_name = 'proxy'
admin.autodiscover()
proxy_api = views.proxy_view()

urlpatterns = [
    url(r'^api/getDownUrl/$', proxy_api.getDownUrl, name='api_getDownUrl'),
    url(r'^api/dopackage/$', proxy_api.dopackage, name='api_dopackage'),
    url(r'^api/get_build_proxy_status/$', proxy_api.get_build_proxy_status, name='api_get_build_proxy_status'),
    url(r'^build/$', proxy_api.getDownUrl, name='api_getDownUrl'),
]
