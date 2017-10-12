from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import Context, loader
from mtaupload.models import Category, File
from django.db.models import  Q

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
    try:
        data = []
        categories = Category.objects.all()
        if categories:
            for category in categories:
                files = File.objects.filter(category_id=category.id)
                category_data = {}
                category_data['category'] = category
                category_data['files'] = files
                if category_data:
                    data.append(category_data)
    except Category.DoesNotExist:
        data = None

    return render(request, 'mtaweb/download.html', {
        'data': data
    })


    # categories = Category.objects.filter(user=request.user)
    # file_results = File.objects.all()
    # query = request.GET.get("q")
    # if query:
    #     categories = categories.filter(
    #         Q(category_title__icontains=query) |
    #         Q(provider__icontains=query)
    #     ).distinct()
    #     file_results = file_results.filter(
    #         Q(filename__contains=query)
    #     ).distinct()
    #     return render(request, 'mtaweb/download.html', {
    #         'categories': categories,
    #         'files': file_results,
    #     })
    # else:
    #     return render(request, 'mtaweb/download.html', {'categories': categories})

    # template = loader.get_template("mtaweb/download.html")
    # return HttpResponse(template.render())
    # return render(request=request, template_name='mtaweb/download.html')
    # return render_to_response('mtaweb/download.html')
