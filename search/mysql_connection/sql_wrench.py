from pymysql import connect


# mysql = connect(
#     host='117.72.37.186',
#     port=3306,
#     user='root',
#     passwd='wu272515.',
#     database='search_engine',
#     charset='utf8mb4',
# )
mysql = connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='111111',
    database='search_engine',
    charset='utf8mb4',
)