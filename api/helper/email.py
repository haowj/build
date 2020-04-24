# coding:utf-8
__author__ = 'xcma'
from django.conf import settings  # 导入配置文件
from django.core.mail import send_mail  # 导入发送邮件的包
import logging
log = logging.getLogger(__name__)

class mail:

    def __init__(self):
        self.send_title = '加载器报警'
        self.send_message = '邮件内容'
        self.send_obj_list = ['maxc@supervcloud.com']  # 收件人列表
        self.send_html_message = ''

    def setTitle(self,title):
        self.send_title =title

    def setSendMessage(self,message):
        self.send_message=message

    def setObjList(self,recv_list):
        if isinstance(recv_list,list):
            for i in recv_list:
                if i not in self.send_obj_list:
                    self.send_obj_list.append(i)

    def setBody(self):

        self.body = """
        <div class="panel panel-danger">
        <div class="panel-title">
            """ + self.send_title + """
        </div>
        <div class="panel-body">
            """ + self.send_message + """
        </div>
        </div>
        """
        return self.body

    def setHtmlMessage(self,body):
        """
           # <div class="panel">
    #     <div class="panel-title">
    #         测试标题
    #     </div>
    #     <div class="panel-body">
    #         测试内容
    #     </div>
    # </div>
    # <div class="panel panel-success">
    #     <div class="panel-title">
    #         测试标题
    #     </div>
    #     <div class="panel-body">
    #         测试内容
    #     </div>
    # </div>
        :return:
        """
        self.send_html_message = """
        <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8" />
        <title>"""+self.send_title+""""</title>
        <style>
            .panel {
                width: 300px;
                margin: 20px;
                border-radius: 4px;
                border: 1px solid #bce8f1;
            }
            .panel-title {
                padding: 10px 15px;
                color: #31708f;
                background-color: #d9edf7;
                border-color: #bce8f1;
                border-radius: 4px 4px 0 0;
            }
            .panel-success {
                border: 1px solid #d6e9c6;
            }
            .panel-success .panel-title {
                color: #3c763d;
                background-color: #dff0d8;
                border-color: #d6e9c6;
            }
            .panel-success .panel-body {
                color: #468847;
            }
            .panel-danger {
                border: 1px solid #ebccd1;
            }
            .panel-danger .panel-title {
                color: #a94442;
                background-color: #f2dede;
                border-color: #ebccd1;
            }
            .panel-danger {
                color: #b94a48;
            }
            .panel-body {
                padding: 15px;
                font-size: 30px;
                color: block;
                text-align:left;
                
            }
            
        </style>
    </head>
    <body>
    """+body+"""
    </body>
    </html>"""

    def setHtmlMessageTable(self):
        self.send_html_message = """
        <html><head><style type="text/css">.table{width:100%;max-width:100%;margin-bottom:20px;border-collapse:collapse;background-color:transparent}td{padding:8px;line-height:1.42857143;vertical-align:top;border:1px solid #ddd;border-top:1px solid #ddd}.table-bordered{border:1px solid #ddd}</style></head><body><h3>发布基本信息</h3><table class="table table-bordered"><tr><td width="10%"><b>AppId</b></td><td width="15%">#{appId}</td><td width="10%"><b>环境</b></td><td width="15%">#{env}</td><td width="10%"><b>集群</b></td><td width="15%">#{clusterName}</td><td width="10%"><b>Namespace</b></td><td width="15%">#{namespaceName}</td></tr><tr><td><b>发布者</b></td><td>#{operator}</td><td><b>发布时间</b></td><td>#{releaseTime}</td><td><b>发布标题</b></td><td>#{releaseTitle}</td><td><b>备注</b></td><td>#{releaseComment}</td></tr></table>#{diffModule}#{rulesModule}<br><a href="#{apollo.portal.address}/config/history.html?#/appid=#{appId}&env=#{env}&clusterName=#{clusterName}&namespaceName=#{namespaceName}&releaseHistoryId=#{releaseHistoryId}">点击查看详细的发布信息</a><br><br>如有Apollo使用问题请先查阅<a href="http://conf.ctripcorp.com/display/FRAM/Apollo">文档</a>，或直接回复本邮件咨询。</body></html>
    """


    def sendmail(self):
        log.debug('sendmail send_title:{};send_message:{};send_obj_list:{}'.format(self.send_title, self.send_message, self.send_obj_list))
        send_status = send_mail(self.send_title, self.send_message, settings.EMAIL_FROM, self.send_obj_list, html_message=self.send_html_message)
        return send_status # 发送状态,可用可不用