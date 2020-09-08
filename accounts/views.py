from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponse

# Create your views here.


def persona_login(request):
    authenticate(assertion=request.POST['assertion'])
    return HttpResponse()
