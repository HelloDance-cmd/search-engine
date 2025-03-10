# from mysql.connector import connect
import MySQLdb

from dbutils.pooled_db import PooledDB


pool = PooledDB(
    creator=MySQLdb,    # 数据库驱动，使用 MySQLdb 连接 MySQL 数据库
    maxconnections=10,   # 连接池中允许的最大连接数
    mincached=2,         # 初始化时创建的空闲连接数
    maxcached=5,         # 连接池中空闲连接的最大数量
    maxshared=3,         # 连接池中共享连接的最大数目
    blocking=True,       # 如果没有可用连接时，是否阻塞等待
    host='localhost',    # 数据库主机地址
    user='root',# 数据库用户名
    passwd='111111', # 数据库密码
    db='search_engine',  # 数据库名
    port=3306            # 数据库端口
)

# 获取连接
def get_conn():
    return pool.connection()

    # 你可以将这个函数(get_conn)添加到你的ORM或DAO层中，以便在需要时获取数据库连接

# mysql = connect(
#     host='117.72.37.186',
#     port=3306,
#     user='root',
#     passwd='wu272515.',
#     database='search_engine',
#     connect_timeout=30000
# )