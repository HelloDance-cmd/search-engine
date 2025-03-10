from search.mysql_connection import mysql


def user_table_verify(userName: str, password: str) -> bool:
  cursor = mysql.cursor()
  
  cursor.execute('SELECT user_name, password FROM user')

  (t_userName, t_password) = cursor.fetchone()
  
  cursor.close()
  return t_userName == userName and t_password == password