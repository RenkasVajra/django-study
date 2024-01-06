from django.shortcuts import render, redirect


def index_page(request):
    return render(request, 'index.html')


def demand(request):
    return render(request, 'demand.html')

