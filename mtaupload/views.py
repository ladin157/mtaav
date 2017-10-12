from django.shortcuts import render, get_object_or_404
from django.db.models import  Q
from .forms import CategoryForm, FileForm, UserForm
from .models import Category, File
from django.http import JsonResponse
from django.contrib.auth import logout, login, authenticate

# AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
# IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# Create your views here.

def create_category(request):
    if not request.user.is_authenticated():
        return render(request, 'mtaupload/login.html')
    else:
        form = CategoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            category = form.save(commit=True)
            category.user = request.user
            category.category_logo = request.FILES['category_logo']
            # file_type = category.category_logo.url.split('.')[-1]
            # file_type = file_type.lower()
            # if file_type not in IMAGE_FILE_TYPES:
            #     context = {
            #         'category': category,
            #         'form': form,
            #         'error_message':'Image file must be PNG, JPG, or JPEG',
            #     }
            #     return render(request, 'mtaupload/create_category.html', context)
            category.save()
            return render(request, 'mtaupload/detail.html', {'category':category})
        context = {'form':form}
        return render(request, 'mtaupload/create_category.html', context)

def create_file(request, category_id):
    form = FileForm(request.POST or None, request.FILES or None)
    category = get_object_or_404(Category, pk = category_id)
    if form.is_valid():
        category_files = category.file_set.all()
        for s in category_files:
            if s.filename == form.cleaned_data.get("filename"):
                context = {
                    'category': category,
                    'form': form,
                    'error_message': 'You already added that file',
                }
                return render(request, 'mtaupload/create_file.html', context)
        file = form.save(commit=False)
        file.category = category
        file.data_file = request.FILES['data_file']
        # file_type = file.data_file.url.split('.')[-1]
        # file_type = file_type.lower()
        # if file_type not in AUDIO_FILE_TYPES:
        #     context = {
        #         'category': category,
        #         'form': form,
        #         'error_message': 'Audio file must be WAV, MP3, or OGG',
        #     }
        #     return render(request, 'mtaupload/create_file.html', context)

        file.save()
        return render(request, 'mtaupload/detail.html', {'category': category})
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'mtaupload/create_file.html', context)

def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    category.delete()
    categogies = Category.objects.filter(user=request.user)
    return render(request, 'mtaupload/index.html', {'categories': categogies})


def delete_file(request, category_id, file_id):
    category = get_object_or_404(Category, pk=category_id)
    file = File.objects.get(pk=file_id)
    file.delete()
    return render(request, 'mtaupload/detail.html', {'category': category})


def detail(request, category_id):
    if not request.user.is_authenticated():
        return render(request, 'mtaupload/login.html')
    else:
        user = request.user
        category = get_object_or_404(Category, pk=category_id)
        return render(request, 'mtaupload/detail.html', {'category': category, 'user': user})


def favorite(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    try:
        if file.is_favorite:
            file.is_favorite = False
        else:
            file.is_favorite = True
        file.save()
    except (KeyError, File.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    try:
        if category.is_favorite:
            category.is_favorite = False
        else:
            category.is_favorite = True
        category.save()
    except (KeyError, Category.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'mtaupload/login.html')
    else:
        categories = Category.objects.filter(user=request.user)
        file_results = File.objects.all()
        query = request.GET.get("q")
        if query:
            categories = categories.filter(
                Q(category_title__icontains=query) |
                Q(provider__icontains=query)
            ).distinct()
            file_results = file_results.filter(
                Q(filename__contains=query)
            ).distinct()
            return render(request, 'mtaupload/index.html', {
                'categories': categories,
                'files': file_results,
            })
        else:
            return render(request, 'mtaupload/index.html', {'categories': categories})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'mtaupload/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                categories = Category.objects.filter(user=request.user)
                return render(request, 'mtaupload/index.html', {'categories': categories})
            else:
                return render(request, 'mtaupload/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'mtaupload/login.html', {'error_message': 'Invalid login'})
    return render(request, 'mtaupload/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                categories = Category.objects.filter(user=request.user)
                return render(request, 'mtaupload/index.html', {'categories': categories})
    context = {
        "form": form,
    }
    return render(request, 'mtaupload/register.html', context)


def files(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'mtaupload/login.html')
    else:
        try:
            file_ids = []
            for category in Category.objects.filter(user=request.user):
                for file in category.file_set.all():
                    file_ids.append(file.pk)
            users_files = File.objects.filter(pk__in=file_ids)
            if filter_by == 'favorites':
                users_files = users_files.filter(is_favorite=True)
        except Category.DoesNotExist:
            users_files = []
        return render(request, 'mtaupload/files.html', {
            'file_list': users_files,
            'filter_by': filter_by,
        })
