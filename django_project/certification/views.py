from django.shortcuts import render
from django.http import HttpResponse


def index(request):

    return HttpResponse("Certification index.")


def homepage_view(request):
    return render(request, 'layouts/homepage.html')
