from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import Context, loader

# Create your views here.

def index(request):
    template = loader.get_template("mtaweb/index.html")
    return HttpResponse(template.render())
    # return render_to_response('mtaweb/index.html')
    # return  HttpResponse("Hello, world. You're at the mtaweb index")

def introduction(request):
    # return redirect('introduction')
    template = loader.get_template("mtaweb/introduction.html")
    return HttpResponse(template.render())
    # return render(request=request, template_name='mtaweb/introduction.html')
    # return render_to_response('mtaweb/introduction.html')

def download(request):
    template = loader.get_template("mtaweb/download.html")
    return HttpResponse(template.render())
    # return render(request=request, template_name='mtaweb/download.html')
    # return render_to_response('mtaweb/download.html')
