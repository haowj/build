# coding:utf-8
__author__ = 'xcma'

from django.conf.urls import url
from django.contrib import admin
from . import views
admin.autodiscover()
app_name = 'api'
vcv = views.version_contorl_view()

urlpatterns = [
    url(r'^sapiloaderAdd/$', vcv.sapiloaderAdd, name='sapiloaderAdd'),
    url(r'^sapiloader_c_build/$', vcv.sapiloader_c_build, name='sapiloader_c_build'),
    url(r'^sapiloader_c_build_result/$', vcv.sapiloader_c_build_result, name='sapiloader_c_build_result'),
    url(r'^dev_model_add/$', vcv.dev_model_add, name='ap_model_add'),
    url(r'^oem_add/$', vcv.oem_add, name='oem_add'),
    url(r'^superdcfAdd/$', vcv.superdcfAdd, name='superdcfAdd'),
    url(r'^zdpi_sig_add/$', vcv.zdpi_sig_add, name='zdpi_sig_add'),
    url(r'^superctlAdd/$', vcv.superctlAdd, name='superctlAdd'),
    url(r'^supertackAdd/$', vcv.supertackAdd, name='supertackAdd'),
    url(r'^superd_build/$', vcv.superd_build, name='superd_build'),
    url(r'^superd_build_test/$', vcv.superd_build_test, name='superd_build_test'),
    url(r'^superd_build_result/$', vcv.superd_build_result, name='superd_build_result'),
    url(r'^packageconfigAdd/$', vcv.packageconfigAdd, name='packageconfigAdd'),
    url(r'^package/$', vcv.package, name='package'),
    url(r'^release/$', vcv.release, name='release'),
    url(r'^restart/$', vcv.restart, name='restart'),
    url(r'^tag_add/$', vcv.tag_add, name='tag_add'),
    url(r'^tag_info/$', vcv.tag_info, name='tag_info'),
    url(r'^build_info/$', vcv.build_info, name='build_info'),
    url(r'^getSuperdInfo/$', vcv.getSuperdInfo, name='getSuperdInfo'),
    url(r'^getConnector/$', vcv.getConnector, name='getConnector'),
    url(r'^getPackageConfigList/$', vcv.getPackageConfigList, name='getPackageConfigList'),
    url(r'^getPackageConfigInfo/$', vcv.getPackageConfigInfo, name='getPackageConfigInfo'),
    url(r'^getadvertising/$', vcv.getadvertising, name='getadvertising'),
    url(r'^advertisingAdd/$', vcv.advertisingAdd, name='advertisingAdd'),
    url(r'^getAdvertisingContent/$', vcv.getAdvertisingContent, name='getAdvertisingContent'),
    url(r'^getPackageInfo/$', vcv.getPackageInfo, name='getPackageInfo'),
    url(r'^getPackageInfo_detail/$', vcv.getPackageInfo_detail, name='getPackageInfo_detail'),
    url(r'^getReleaseInfo/$', vcv.getReleaseInfo, name='getReleaseInfo'),
    url(r'^getPackageIDInfo/$', vcv.getPackageIDInfo, name='getPackageIDInfo'),
    url(r'^deltag/$', vcv.deltag, name='deltag'),
    url(r'^connector_add/$', vcv.connector_add, name='connector_add'),
    # url(r'^authadd/$', vcv.authadd, name='authadd'),
    # url(r'^show_progress/$', timetask.show_progress, name='show_progress'),

]