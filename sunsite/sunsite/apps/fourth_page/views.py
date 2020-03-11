from django.shortcuts import render
from django.http import HttpResponse
import requests


def main(request):
    context = {}
    return render(request, 'fourth_page/fourth_page.html', context)

