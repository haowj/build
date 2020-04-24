#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import redis


class ConnectRedis:
    def __init__(self):
        pool = redis.ConnectionPool(host='127.0.0.1', port='6379', decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)

    "redis基本命令 String"

    def pipe(self):
        """
        管道技术，
        :return:
        """
        self.p = self.r.pipeline()

    def pipe_get(self):
        self.p.get()
        self.p.execute()

    def get(self, k):
        return self.r.get(k)

    def set(self, k, v):
        return self.r.set(k, v)

    def smembers(self, k):
        return self.r.smembers(k)

    def setex(self, k, v, t):
        # t秒后，取值就从v变成None
        return self.r.setex(k, v, t)

    def psetex(self, k, v, t):
        # t毫秒后，取值就从v变成None
        return self.r.psetex(k, t, v)

    def setnx(self, k, v):
        # 设置值，只有k不存在时，执行设置操作（添加）
        return self.r.setnx(k, v)

    def setxx(self, k, v):
        # 如果设置为True，则只有k存在时，当前set操作才执行 （修改）
        return self.r.set(k, v, xx=True)

    def mset(self, *args, **kwargs):
        # 批量设置值
        return self.r.mset(*args, **kwargs)

    def msetnx(self, *args, **kwargs):
        # 批量设置值,不存在，则执行
        return self.r.msetnx(*args, **kwargs)

    def mget(self, k, *args):
        # 批量获取
        return self.r.mget(k, *args)

    def getset(self, k, v):
        # 设置新值并获取原来的值
        return self.r.getset(k, v)

    def setrange(self, k, offset, v):
        """
        修改字符串内容，从指定字符串索引开始向后替换（新值太长时，则向后添加）
        参数：
        offset，字符串的索引，字节（一个汉字三个字节）
        value，要设置的值
         # jccci 原始值是junxi 从索引号是1开始替换成ccc 变成 jccci
        :param k:
        :param offset:
        :param v:
        :return:
        """
        return self.r.setrange(k, offset, v)

    def getrange(self, k, start, end):
        """
        获取子序列（根据字节获取，非字符）
        参数：
        name，Redis 的 name
        start，起始位置（字节）
        end，结束位置（字节）
        如： "君惜大大" ，0-3表示 "君"  、、一个中文占3个字节

        :return:
        """
        return self.r.getrange(k, start, end)

    def strlen(self, k):
        # 返回name对应值的字节长度（一个汉字3个字节）
        return self.r.strlen(k)

    def incr(self, name, amount=1):
        """
        自增 name对应的值，当name不存在时，则创建name＝amount，否则，则自增。
        参数：
        name,Redis的name
        amount,自增数（必须是整数）
        注：同incrby
        :param name:
        :param amount:
        :return:
        """
        return self.r.incr(name, amount)

    def incrbyfloat(self, name, amount=1.0):
        """
        自增 name对应的值，当name不存在时，则创建name＝amount，否则，则自增。
        参数：
        name,Redis的name
        amount,自增数（浮点型）
        """
        return self.r.incrbyfloat(name, amount)

    def decr(self, name, amount=1):
        """
        自减 name对应的值，当name不存在时，则创建name＝amount，否则，则自减。
        参数：
        name,Redis的name
        amount,自减数（整数)
        """
        return self.r.decr(name, amount)

    def append(self, k, v):
        """
        在redis name对应的值后面追加内容
        参数：
        key, redis的name
        value, 要追加的字符串
        """
        return self.r.append(k, v)

    """redis 操作 hash """

    def hset(self, name, k, v):
        """
        1.单个增加--修改(单个取出)--没有就新增，有的话就修改
        hset(name, key, value)
        name对应的hash中设置一个键值对（不存在，则创建；否则，修改）
        参数：
        name，redis的name
        key，name对应的hash中的key
        value，name对应的hash中的value
        注：
        hsetnx(name, key, value),当name对应的hash中不存在当前key时则创建（相当于添加）
        :return:
        """
        return self.r.hset(name,k, v)

    def hmset(self,name,mapping):
        """
        hmset(name, mapping)
        在name对应的hash中批量设置键值对
        参数：
        name，redis的name
        mapping，字典，如：{'k1':'v1', 'k2': 'v2'}
        如：
        r.hmset("hash2", {"k2": "v2", "k3": "v3"})
        """
        return self.r.hmset(name,mapping)

    def hget(self,name,k):
        """在name对应的hash中获取根据key获取value"""
        return self.r.hget(name,k)

    def hmget(self,name,keys,*args):
        """
        hmget(name, keys, *args)
        在name对应的hash中获取多个key的值
        参数：
        name，reids对应的name
        keys，要获取key集合，如：['k1', 'k2', 'k3']
        *args，要获取的key，如：k1,k2,k3
        如：
        print(r.hget("hash2", "k2"))  # 单个取出"hash2"的key-k2对应的value
        print(r.hmget("hash2", "k2", "k3"))  # 批量取出"hash2"的key-k2 k3对应的value --方式1
        print(r.hmget("hash2", ["k2", "k3"]))  # 批量取出"hash2"的key-k2 k3对应的value --方式2

        """
        return self.r.hmget(name,keys,*args)

    def hgetall(self,name):
        """
        取出所有的键值对
        hgetall(name)
        获取name对应hash的所有键值
        """
        return self.r.hgetall(name)

    def hlane(self,name):
        """
        hlen(name)
        获取name对应的hash中键值对的个数
        """
        return self.r.hlen(name)

    def hkeys(self,name):
        """
        hkeys(name)
        获取name对应的hash中所有的key的值
        :return:
        """
        return self.r.hkeys(name)

    def hvals(self,name):
        """
        获取name对应的hash中所有的value的值
        :return: 
        """
        return self.r.hvals(name)

    def hexists(self,name,key):
        """
        检查name对应的hash是否存在当前传入的key
        :return: 
        """
        return self.r.hexists(name,key)

    def hdel(self,name,*keys):
        """
        将name对应的hash中指定key的键值对删除
        :param name:
        :param keys:
        :return:
        """
        return self.r.hdel(name,*keys)

    def hincrby(self,name, key, amount=1):
        """
        自增name对应的hash中的指定key的值，不存在则创建key=amount
        参数：
        name，redis中的name
        key， hash对应的key
        amount，自增数（整数）
        :param name:
        :param key:
        :param amount:
        :return:
        """
        return self.r.hincrby(name,key,amount)

    def hincrbyfloat(self,name, key, amount=1.0):
        """
        将key对应的value--浮点数 自增1.0或者2.0，或者别的浮点数 负数就是自减
        自增name对应的hash中的指定key的值，不存在则创建key=amount
        参数：
        name，redis中的name
        key， hash对应的key
        amount，自增数（浮点数）
        自增name对应的hash中的指定key的值，不存在则创建key=amount
        """
        return self.r.hincrbyfloat(name,key,amount)

    def hsetnx(self,name,key,value):
        """
        如果哈希表不存在，一个新的哈希表被创建并进行 HSET 操作。

        如果字段已经存在于哈希表中，操作无效。

        如果 key 不存在，一个新哈希表被创建并执行 HSETNX 命令。
        :param name:
        :param key:
        :param value:
        :return:
        """
        return self.r.hsetnx(name,key,value)

    def hscan(self,name, cursor=0, match=None, count=None):
        """
        增量式迭代获取，对于数据大的数据非常有用，hscan可以实现分片的获取数据，并非一次性将数据全部获取完，从而放置内存被撑爆
        参数：
        name，redis的name
        cursor，游标（基于游标分批取获取数据）
        match，匹配指定key，默认None 表示所有的key
        count，每次分片最少获取个数，默认None表示采用Redis的默认分片个数
        如：
        第一次：cursor1, data1 = r.hscan('xx', cursor=0, match=None, count=None)
        第二次：cursor2, data1 = r.hscan('xx', cursor=cursor1, match=None, count=None)
        ...
        直到返回值cursor的值为0时，表示数据已经通过分片获取完毕

        :param name:
        :param cursor:
        :param match:
        :param count:
        :return:
        """
        return self.r.hscan(name, cursor, match, count)

    def hscan_iter(self,name, match=None, count=None):
        """
        利用yield封装hscan创建生成器，实现分批去redis中获取数据
        参数：
        match，匹配指定key，默认None 表示所有的key
        count，每次分片最少获取个数，默认None表示采用Redis的默认分片个数
        如：
        :param name:
        :param match:
        :param count:
        :return:
        """
        return self.r.hscan_iter(name,match,count)

    """ 其他常用操作 """
    def delete(self,*names):
        """
        根据删除redis中的任意数据类型（string、hash、list、set、有序set）
        :param name:
        :return:
        """
        return self.r.delete(*names)

    def exists(self,name):
        """
        检测redis的name是否存在，存在就是True，False 不存在
        :param name:
        :return:
        """
        return self.r.exists(name)

    def keys(self,pattern=''):
        """
        根据模型获取redis的name
        更多：
        KEYS * 匹配数据库中所有 key 。
        KEYS h?llo 匹配 hello ， hallo 和 hxllo 等。
        KEYS hllo 匹配 hllo 和 heeeeello 等。
        KEYS h[ae]llo 匹配 hello 和 hallo ，但不匹配 hillo
        :param pattern:
        :return:
        """
        return self.r.keys(pattern)

    def expire(self,name ,time):
        """
        为某个redis的某个name设置超时时间
        :param name:
        :param time:
        :return:
        """
        return self.r.expire(name,time)

    def rename(self,oldname,newname):
        """
        对redis的name重命名
        r.lpush("list5", 11, 22)
        r.rename("list5", "list5-1")
        :return: 
        """
        return self.r.rename(oldname,newname)

    def randomkey(self):
        """
        随机获取一个redis的name（不删除）
        :return:
        """
        return self.r.randomkey()

    def type(self,name):
        """P
        获取name对应值的类型
        """
        return self.r.type(name)


rs_conn = ConnectRedis()
