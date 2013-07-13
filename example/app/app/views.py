from django.shortcuts import render

from app.models import Stock

def index(request):
    #latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': 'bla'}
    return render(request, 'app/index.html', context)

def add_stock(request):
    print 12
    return index(request)
