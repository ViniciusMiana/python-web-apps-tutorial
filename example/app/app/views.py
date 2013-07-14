from django.shortcuts import render, redirect
from django.http import HttpResponse

from httplib import HTTPConnection

from app.models import Stock

def index(request):

    if request.method == 'POST':
        return add_stock(request)

    context = {'stock_list': Stock().list_stocks()}

    return render(request, 'app/index.html', context)

def add_stock(request):

    conn = HTTPConnection("localhost", 8080)
    conn.request("POST", "/stock/{0}".format(request.POST["stock"]))
    response = conn.getresponse()

    if response.status != 200:
        return HttpResponse(str(response.read()))

    return redirect("/")

def remove_stock(request, stock):

    conn = HTTPConnection("localhost", 8080)
    conn.request("DELETE", "/stock/{0}".format(stock))
    response = conn.getresponse()

    return redirect("/")