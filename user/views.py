from django.http import HttpRequest, JsonResponse

import hashlib
import json

from search.models import User

def userPermissionView(request: HttpRequest):
  ...


def user_login_view(request: HttpRequest):
  """验证用户登录是否合法

  Args:
      request (HttpRequest): request请求

  Returns:
      JsonResponse: 正确与否
  """
  # request.POST.get()
  json_data = json.loads(request.body)
  # user_name = request.POST.get('username')
  # password = request.POST.get('password')

  user_name = json_data["username"]
  password = str(json_data['password'])

  # md5加密
  encrypt_password = hashlib.md5(password.encode('utf-8')).hexdigest()

  user = User.objects.filter(name=user_name).first()

  if user is None:
    return JsonResponse({
      'message': 'False'
    }) 

  return JsonResponse({
    'message': str(user.password == encrypt_password)
  })



def user_register_view(request: HttpRequest):
  """验证用户注册是否合法，如果合法则对用户进行注册

  Args:
      request (HttpRequest): request请求

  Returns:
      JsonResponse: 正确与否
  """
  json_data = json.loads(request.body)
  # userName = request.POST.get('username')
  # password = request.POST.get('password')
  print(json_data)
  user_name = str(json_data["username"])
  password = str(json_data['password'])
  email = str(json_data['email'])

  # userName = request.POST.get('username')
  # password = request.POST.get('password')
  
  # md5加密
  encrypt_password = hashlib.md5(password.encode('utf-8')).hexdigest()
  user = User.objects.filter(name=user_name).first()  

  if user is not None:
    return JsonResponse({
      "message": '该用户已经存在，无法注册'
    })

  new_user_account = User()
  new_user_account.email = None if email == 'None' else email
  new_user_account.name = user_name
  new_user_account.password = encrypt_password
  new_user_account.avatar = ''
  new_user_account.save()

  return JsonResponse({
    'message': 'True'
  })