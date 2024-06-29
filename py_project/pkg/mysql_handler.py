# -*- coding: utf8 -*-

import pymysql
from dbutils.pooled_db import PooledDB, SharedDBConnection

class ServerError(Exception):
    pass

class MysqlHandler(object):
    """
    操作MySQL数据库的工具类
    """

    def __init__(self, mysql_info):
        """
        初始化方法,创建数据库连接池
        :param mysql_info: 数据库连接信息
        """
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=mysql_info.get("pool_size"),
            mincached=2,
            maxcached=5,
            maxshared=3,
            blocking=True,
            maxusage=None,
            setsession=[],
            ping=0,
            host=mysql_info.get("host"),
            port=mysql_info.get("port"),
            user=mysql_info.get("user"),
            password=mysql_info.get("password"),
            database=mysql_info.get("database"),
            charset='utf8'
        )

    def get_conn(self):
        """
        从连接池中获取一个数据库连接
        :return: 数据库连接对象
        """
        return self.pool.connection()

    def excute_sql(self, sql, data):
        """
        执行SQL插入、更新或删除操作
        :param sql: SQL语句
        :param data: SQL参数
        :return: None
        """
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, data)
                conn.commit()
        except Exception as e:
            conn.rollback()
            err_msg = "excute mysql sql error {e}".format(e=str(e))
            raise ServerError(err_msg)
        finally:
            conn.close()

    def query_sql_all(self, sql, data=None):
        """
        执行SQL查询操作,返回所有结果
        :param sql: SQL语句
        :param data: SQL参数
        :return: 查询结果列表
        """
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
        except Exception as e:
            err_msg = "query mysql sql error {e}".format(e=str(e))
            raise ServerError(err_msg)
        finally:
            conn.close()
        return result

    def query_sql(self, sql, data=None):
        """
        执行SQL查询操作,返回第一个结果
        :param sql: SQL语句
        :param data: SQL参数
        :return: 第一个查询结果
        """
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchone()
        except Exception as e:
            err_msg = "query mysql sql error {e}".format(e=str(e))
            raise ServerError(err_msg)
        finally:
            conn.close()
        return result