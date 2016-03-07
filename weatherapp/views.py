from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. Only two kinds of weather types excist: Clear and Non-clear.")
