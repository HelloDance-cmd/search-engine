from django.http import HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    print('Request for ', request.get_host() + request.get_port())
    return render(request, 'index.html')

