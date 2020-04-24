#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from django.db import connection


def get_value_list(sql):
    """
    获取值列表信息
    """
    if sql:
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        except Exception:
            return None
    else:
        return None
