from django.shortcuts import render

def hello(request, data):   
    return render(request,'hello/hello.html', {'data': data})