#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'

from strategy.models import *
from appack.models import dpiConfigVersion

import logging
log = logging.getLogger(__name__)


def get_data_base(table, *args):
    """
    获取数据的公共方法 获取所以数据，可以指定获取数据的字段
    返回是 dict 对象
    :param table: 表名称
    :param args:  获取指定的是数据字段内容， 空是获取该表的全部字段数据。
    :return:
    """
    try:
        ex_base = eval(table)
        if args:

            data = ex_base.objects.values(*args).order_by(f'-{args[0]}', '-id')
        else:
            data = ex_base.objects.values().order_by('-update_time', '-id')
        return data
    except Exception as e:
        log.error(e)
        return f'error:{e}'


def get_data_base_filter(table, **kwargs):
    """
    获取数据的公共方法 获取条件匹配内容 默认 id倒序排列数据
    返回是 dict 对象
    :param table: 表名称
    :param kwargs:  查询指定数据。
    :return:
    """
    try:
        ex_base = eval(table)
        if kwargs:
            data = ex_base.objects.filter(**kwargs).values().order_by('-update_time', '-id')
        else:
            data = ex_base.objects.values().order_by('-update_time', '-id')
        return data
    except Exception as e:
        log.error(e)
        return f'error:{e}'

def get_data_base_order(table, *args):
    """
    获取数据的公共方法 获取所有数据可以进行字段排序
    返回是 query set 对象
    :param table: 表名称
    :param kwargs:  查询指定数据。
    :return:
    """
    try:
        ex_base = eval(table)
        if args:
            data = ex_base.objects.all().order_by(*args)
        else:
            data = ex_base.objects.all().order_by('-id')
        return data
    except Exception as e:
        log.error(e)

def insert_into_data(table, **kwargs):
    """
    数据插入方法
    返回 元组对象
    :param table:
    :param kwargs:
    :return:
    """
    try:
        ex_base = eval(table)
        if kwargs:
            data = ex_base.objects.update_or_create(**kwargs)
            return data
        else:
            return '参数能为空'
    except Exception as e:
        log.error(e)
        return f'error:{e}'


def get_data_base_one(table, ids):
    """
    获取数据的公共方法 获取所有数据可以进行字段排序
    返回是 query set 对象
    :param table: 表名称
    :param kwargs:  查询指定数据。
    :return:
    """
    try:
        ex_base = eval(table)
        data = ex_base.objects.get(id=ids)
        return data
    except Exception as e:
        log.error(e)
        return f'error:{e}'


def update_data_base_one(table, status, **kwargs):
    """
    获取数据的公共方法 获取所有数据可以进行字段排序
    返回是 query set 对象
    :param table: 表名称
    :param kwargs:  查询指定数据。
    :return:
    """
    try:
        ex_base = eval(table)
        data = ex_base.objects.filter(**kwargs).update(status=status)
        return data
    except Exception as e:
        log.error(e)
        return f'error:{e}'


def exclude_data_base(table, **kwargs):
    """
    不包含过滤数据
    返回是 dict 对象 使用update_time 倒序排序
    :param table:
    :param kwargs:
    :return:
    """
    try:
        ex_base = eval(table)
        data = ex_base.objects.exclude(**kwargs).values().order_by('-update_time', '-id')
        return data
    except Exception as e:
        log.error(e)
        return f'error:{e}'


def get_filter(table, **kwargs):
    """
    获取数据的公共方法 获取条件匹配内容 默认 id倒序排列数据
    返回是 dict 对象
    :param table: 表名称
    :param kwargs:  查询指定数据。
    :return:
    """
    try:
        ex_base = eval(table)
        if kwargs:
            data = ex_base.objects.filter(**kwargs).order_by('update_time', '-id')
        else:
            data = ex_base.objects.all().order_by('-update_time', '-id')
        return data
    except Exception as e:
        log.error(e)


def create_data(table, **kwargs):
    """
    数据插入方法
    返回 元组对象
    :param table:
    :param kwargs:
    :return:
    """
    try:
        ex_base = eval(table)
        if kwargs:
            data = ex_base.objects.create(**kwargs)
            return data
        else:
            return '参数能为空'
    except Exception as e:
        log.error(e)
        return f'error:{e}'
