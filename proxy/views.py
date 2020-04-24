from django.shortcuts import render
from rest_framework.views import APIView
from api.helper.misc import getSign
# Create your views here.
from api.controller.dataToJson import *
from proxy.controller.build import proxy_build_class
import logging
log = logging.getLogger(__name__)
pbc = proxy_build_class()
class Auth:
    def check_sign(self, request):
        para = request.GET
        para_dict = {}
        para_sign = ''
        for k, v in para.items():
            if k != 'sign':
                para_dict[k] = v
            else:
                para_sign = v
        sign = getSign(para_dict)
        if sign == para_sign:
            log.debug('鉴权成功')
            return True
        log.debug('鉴权失败：{}={}?{}'.format(sign, para_sign, sign == para_sign))
        return False

    def login_auth(self,request):
        authent = False
        if request.user.is_authenticated:
            authent=True
        return authent

class proxy_view(APIView):
    auth = Auth()
    def  getDownUrl(self,request):
        if self.auth.check_sign(request):
            dev_model = request.GET.get('dev_model')
            # data = {'dev_model':dev_model,'down_load_url':'http://plug.superhcloud.com/proxy','md5':'123123231231231'}
            data = pbc.get_dev_model_proxy(dev_model)
            return JsonResponse(data)
        return JsonError('鉴权失败')

    def dopackage(self,request):
        if self.auth.login_auth(request):
            dev_model = request.GET.get('dev_model')
            data = pbc.dobuid(dev_model,str(request.user))
            return JsonResponse(data)
        return JsonError('鉴权失败')

    def get_build_proxy_status(self,request):
        if self.auth.login_auth(request):
            dev_model = request.GET.get('dev_model')
            data = pbc.get_proxy(dev_model,str(request.user))
            return JsonResponse(data)
        return JsonError('鉴权失败')


class proxy_web_view:
    auth = Auth()
    def proxy_build(self,request):
       pass
