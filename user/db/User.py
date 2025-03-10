
from rebuild_search.mysql_connection.sql_wrench import get_conn

mysql = get_conn()


def verify_user(username: str, password: str) -> bool:
    """验证用户名和密码是否合法

    Args:
        username (str): 用户名
        password (str): 密码

    Returns:
        bool: 是否合法如果为true则表明合法
    """
    cursor = mysql.cursor()
    sql = "SELECT * FROM `user` WHERE u_name = '%s' AND u_password = '%s'" % (username, password)
    affect_rows = cursor.execute(sql)
    cursor.fetchall()
    
    return affect_rows == 1


def insert_to_user_tb(username: str, password: str) -> bool:
    """添加到用户表中

    Args:
        username (str): 用户名
        password (str): 密码

    Returns:
        bool: 是否添加成功
    """

    cursor = mysql.cursor()
    sql = "INSERT INTO `user`(u_name, u_password) VALUE('%s', '%s')" % (username, password)
    affect_rows = cursor.execute(sql)

    mysql.commit()

    return affect_rows == 1