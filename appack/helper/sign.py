# coding:utf-8
__author__ = 'xcma'
import logging,hashlib
log = logging.getLogger(__name__)

def getSign(param):
    """md5($mobile.$mac.'pythonapi')"""
    ps = ''
    pdict = sorted(param.items(), key=lambda param:param[0], reverse=False)
    log.debug(pdict)
    for i in pdict:
        ps +='{}={}'.format(i[0].lower(),i[1])
    cmd = 'pythonapi{}'.format(ps)
    log.debug('str:{}'.format(cmd))
    sign = hashlib.md5(cmd.encode('utf-8')).hexdigest()
    log.debug(sign)
    return sign

def check_sign(request):
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