from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest

import hashlib
import json

from modules.models import User

def userPermissionView(request: HttpRequest):
  ...


def user_login_view(request: HttpRequest):
  if request.method != 'POST':
    return HttpResponseBadRequest('请求格式必须是POST')

  data = json.loads(request.body)
  user_name = data['username'].__str__()
  password = data['password'].__str__()

  if not user_name or not password:
    return HttpResponseBadRequest('用户名密码必须同时存在')

  # json_data = json.loads(request.body)
  # user_name = json_data["username"]
  # password = str(json_data['password'])

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
  if request.method != 'POST':
    return JsonResponse({
      "message": '请求格式必须是POST'
    })

  data = json.loads(request.body)
  user_name = data['username'].__str__()
  password = data['password'].__str__()
  data.setdefault('email', 'default@email')
  email = data['email'].__str__()

  # json_data = json.loads(request.body)
  # user_name = str(json_data["username"])
  # password = str(json_data['password'])
  # email = str(json_data['email'])
  # md5加密
  user = User.objects.filter(name=user_name).first()

  if user is not None:
    return JsonResponse({
      "message": '该用户已经存在，无法注册'
    })

  encrypt_password = hashlib.md5(password.encode('utf-8')).hexdigest()
  new_user_account = User()
  new_user_account.email = None if email == 'None' else email
  new_user_account.name = user_name
  new_user_account.password = encrypt_password
  new_user_account.avatar = ''
  new_user_account.save()

  return JsonResponse({
    'message': "True"
  })