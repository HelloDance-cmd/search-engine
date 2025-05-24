import hashlib
import json
import jwt

from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponse

from modules.GlobalHttpStatusCode import HttpStatusCode
from modules.models import User


def user_login_view(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponseBadRequest('请求格式必须是POST')

    data = json.loads(request.body)
    user_name = data['username'].__str__()
    password = data['password'].__str__()

    if not user_name or not password:
        return HttpResponseBadRequest('用户名密码必须同时存在')

    # md5加密
    encrypt_password = hashlib.md5(password.encode('utf-8')).hexdigest()

    user = User.objects.filter(name=user_name).first()
    
    if user is None:
        return JsonResponse({
            'message': 'False'
        })

    return JsonResponse({
        'message': str(user.password == encrypt_password),

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


def NOT_SUPPORTED_THIS_REQUEST():
    return HttpResponseBadRequest('你的请求可能存在问题，请检查参数或者是请求方法是否正确')


def get_user_profile(request: HttpRequest):
    user_name = request.GET.get('username')

    if user_name is None or user_name == '':
        return NOT_SUPPORTED_THIS_REQUEST()

    user = User.objects.filter(name=user_name).first()

    if user is None:
        return NOT_SUPPORTED_THIS_REQUEST()

    user_profile = {
        'name': user.name,
        'avatar': user.avatar,
        'email': user.email
    }

    return JsonResponse(user_profile, status=HttpStatusCode.HTTP_200_OK)


def user_change_username(request: HttpRequest):
    your_user_name = request.GET.get('username')
    changed_user_name = request.GET.get('willChangeUsername')

    if not (your_user_name or changed_user_name):
        return NOT_SUPPORTED_THIS_REQUEST()

    user = User.objects.filter(name=your_user_name).first()
    user.name = changed_user_name
    user.save()

    return HttpResponse("修改成功", status=HttpStatusCode.HTTP_200_OK)


def user_change_password(request: HttpRequest):
    if request.body is None:
        return HttpResponseBadRequest(False)

    data = json.loads(request.body)
    if data is None:
        return HttpResponseBadRequest(False)

    user_name = data['userName'].__str__()
    password = data['password'].__str__()

    user = User.objects.filter(name=user_name).first()
    user.password = hashlib.md5(password.encode('utf-8')).hexdigest()
    user.save()

    return HttpResponse(True)

