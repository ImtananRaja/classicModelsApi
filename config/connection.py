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


def _some(param1: int) -> str:
    """

    :type param1: int
    """
    param2 = param1 + 2
    return "hello"


res: str = _some(param1=2)

db: object = _connect()
