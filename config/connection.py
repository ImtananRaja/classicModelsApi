import pymysql


def _connect() -> object:
    """This will connect you to the database"""

    database_conn = pymysql.connect(host="localhost",
                                    user="api",
                                    password="password",
                                    database="classicmodels",
                                    port=3307)
    c = database_conn.cursor()
    return c


def _something(some_param: int) -> str:
    param2 = some_param + 2
    return "hello"


hello_string: str = _something(2)

db: object = _connect()
