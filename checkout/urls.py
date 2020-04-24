from django.urls import path

from checkout.views import checkout_api
from . import views
capi = checkout_api()
app_name = 'checkout'
urlpatterns = [
    # view
    path('showCase/', views.show_case, name='showCase'),
    path('dataCase/', views.data_case, name='dataCase'),
    path('testApList/', views.testApList, name='testApList'),
    path('testSetList/', views.testSetList, name='testSetList'),
    path('testCaseList/', views.testCaseList, name='testCaseList'),
    path('testRecordList/', views.testRecordList, name='testRecordList'),
    path('testApSetList/', views.testApSetList, name='testApSetList'),

    # api
    path('api/get_task/', capi.get_task, name='api_get_task'),  # 客户端获取服务端配置接口
    path('api/getBasicsInfo/', capi.getBasicsInfo_v, name='api_getBasicsInfo'),
    path('api/addBasicsInfo/', capi.addBasicsInfo_v, name='api_addBasicsInfo'),
    path('api/delBasicsInfo/', capi.delBasicsInfo_v, name='api_delBasicsInfo'),
    path('api/getDevModelList/', capi.getDevModelList_v, name='api_getDevModelList'),
    path('api/getTestCaseList/', capi.getTestCaseList_v, name='api_getTestCaseList'),
    path('api/addTestAP/', capi.addTestAP_v, name='api_addTestAP'),
    path('api/addTestCase/', capi.addTestCase_v, name='api_addTestCase'),
    path('api/addTestSet/', capi.addTestSet_v, name='api_addTestSet'),
    path('api/addTestApSet/', capi.addTestApSet_v, name='api_addTestApSet'),
    path('api/upTestAP/', capi.upTestAP_v, name='api_upTestAP'),
    path('api/upTestCase/', capi.upTestCase_v, name='api_upTestCase'),
    path('api/delTestAP/', capi.delTestAP_v, name='api_delTestAP'),
    path('api/delTestAPSetList/', capi.delTestAPSetList_v, name='api_delTestAPSetList'),
    path('api/getTestAPSetListInfo/', capi.getTestAPSetListInfo_v, name='api_getTestAPSetListInfo'),
    path('api/getTestSetListInfo/', capi.getTestSetListInfo_v, name='api_getTestSetListInfo'),
    path('api/delTestCase/', capi.delTestCase_v, name='api_delTestCase'),
    path('api/delTestSet/', capi.delTestSet_v, name='api_delTestSet'),
    path('api/getTestAPInfo/', capi.getTestAPInfo_v, name='api_getTestAPInfo'),
    path('api/runTestAP/', capi.runTestAP_v, name='api_runTestAP'),
    path('api/getTestSet/', capi.getTestSet_v, name='api_getTestSet'),
    path('api/getTestCase/', capi.getTestCase_v, name='api_getTestCase'),
    path('api/getCaseResult/', capi.getCaseResult_v, name='api_getCaseResult'),
    path('api/getRecord/', capi.getRecord_v, name='api_getRecord'),
]