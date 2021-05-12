import pymysql
import traceback
import constant
from module.Error import Error


class Database(object):
    db_connect = None
    db_cursor = None
    __error = Error()

    def __init__(self):
        self.__connect()

    @classmethod
    def __connect(cls):
        try:
            if cls.db_connect is None:
                cls.db_connect = pymysql.connect(host=constant.DB_HOST,
                                                 user=constant.DB_USER,
                                                 password=constant.DB_PASSWORD,
                                                 db=constant.DB_NAME,
                                                 port=int(constant.DB_PORT),
                                                 cursorclass=pymysql.cursors.DictCursor)
                cls.db_cursor = cls.db_connect.cursor()
        except Exception as error_stack:
            error_stack = traceback.format_exc()
            cls.__error.logging(error_stack)

    @classmethod
    def execute(cls, sql):
        try:
            cursor = cls.db_cursor
            cursor.execute(sql)
            result = cursor.fetchall()
            cls.db_connect.commit()
        except Exception as error_stack:
            cls.db_connect.rollback()
            error_stack = traceback.format_exc()
            cls.__error.logging(error_stack)
            result = None

        cls.db_connect.close()
        cls.db_connect = None
        return result

    @classmethod
    def multi_execute(cls, queries):
        try:
            if not isinstance(queries, list):
                return False

            cursor = cls.db_cursor
            for query in queries:
                cursor.execute(query)
        except Exception as error_stack:
            cls.db_connect.rollback()
            error_stack = traceback.format_exc()
            cls.__error.logging(error_stack)
        else:
            cls.db_connect.commit()
        cls.db_connect.close()
        cls.db_connect = None

    @classmethod
    def get_insert_id(cls):
        return cls.db_cursor.lastrowid