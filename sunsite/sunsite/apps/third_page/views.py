from django.shortcuts import render
from django.http import HttpResponse
import requests


def main(request):
    context = {}
    return render(request, 'third_page/third_page.html', context)
