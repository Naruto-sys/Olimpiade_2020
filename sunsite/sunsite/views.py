from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime
import time


def main(request):
    context = {}
    return render(request, 'main_page/main_page.html', context)
