from django.shortcuts import render
from django.http import HttpResponse
import requests


def main(request):
    context = {}
    return render(request, 'fifth_page/fifth_page.html', context)

