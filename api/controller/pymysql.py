# coding:utf-8
__author__ = 'xcma'
import pymysql,logging
log = logging.getLogger(__name__)
import platform
class Mysql:
    def __init__(self):
        self.__connect()
    def __connect(self):
        # 打开数据库 （如果连接失败会报错）
        if platform.system()=='Linux':
            self.db = pymysql.connect(host = '127.0.0.1', port = 3306, user = 'labs', passwd = 'labs@117', db = 'zjzy_base',charset="utf8")
        else:
            self.db = pymysql.connect(host='120.27.21.176', port=3306, user='root', passwd='zjzy@123', db='zjzy_base', charset="utf8")

        # 获取游标对象
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def getVersion(self):
        # 执行sql查询操作
        sql_select = "select version()"
        return self.cursor.execute(sql_select)
    def fetchone(self):
        # 使用fetchone()获取单条数据
        data = self.cursor.fetchone()
        return data

    def getquery(self,sql):
        try:
            # 执行sql
            log.debug(sql)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            log.debug(result)
            return result
        except:
            # 发生异常
            self.db.rollback()

    def setquery(self,sql):
        try:
            self.cursor.execute(sql)
            data =self.db.commit()
            return data
        except:
            self.db.rollback()

    def close(self):
        # 关闭连接
        self.db.close()