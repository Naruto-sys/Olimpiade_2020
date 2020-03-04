from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h6>PRIVET, VALYA!<h6>")
