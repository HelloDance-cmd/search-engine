from django.http import HttpRequest, JsonResponse

import hashlib
import json

from user.db import User

def userPermissionView(request: HttpRequest):
  ...


def userLoginView(request: HttpRequest):
  """验证用户登录是否合法

  Args:
      request (HttpRequest): request请求

  Returns:
      JsonResponse: 正确与否
  """
  json_data = json.loads(request.body)
  # userName = request.POST.get('username')
  # password = request.POST.get('password')

  userName = json_data["username"]
  password = str(json_data['password'])

  # md5加密
  newPassword = hashlib.md5(password.encode('utf-8')).hexdigest()

  is_passed = User.verify_user(userName, newPassword)

  return JsonResponse({
    'message': str(is_passed)
  })



def userRegisterView(request: HttpRequest):
  """验证用户注册是否合法，如果合法则对用户进行注册

  Args:
      request (HttpRequest): request请求

  Returns:
      JsonResponse: 正确与否
  """
  json_data = json.loads(request.body)
  # userName = request.POST.get('username')
  # password = request.POST.get('password')

  userName = json_data["username"]
  password = str(json_data['password'])

  # userName = request.POST.get('username')
  # password = request.POST.get('password')
  
  # md5加密
  newPassword = hashlib.md5(password.encode('utf-8')).hexdigest()
  is_passed = User.verify_user(userName, newPassword)

  if is_passed:
    return JsonResponse({
      "message": '该用户已经存在，无法注册'
    })

  User.insert_to_user_tb(userName, newPassword)
  return JsonResponse({
    'message': str(not is_passed)
  })