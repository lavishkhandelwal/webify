from django.core import paginator
from .models import Ocr
from .utils import execute
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url = '/login/')
def ocr_index(request):
    user = request.user
    img = Ocr.objects.filter(user = user)
    image_paginator = Paginator(img, 3)
    image = request.GET.get('page')
    try:
        image_1 = image_paginator.page(image)
    except PageNotAnInteger:
        image_1 = image_paginator.page(1)
    except EmptyPage:
        image_1 = image_paginator.page(image_paginator.num_pages)
    return render(request, 'ocr.html', {'image':image_1})

@login_required(login_url = '/login/')
def convert(request):
    if request.method == 'POST':
        if len(request.FILES['image']) != 0:
            if not Ocr.objects.filter(name = request.POST['img_name'], user = request.user).exists():
                ocr = Ocr()
                ocr.image = request.FILES['image']
                ocr.name = request.POST['img_name']
                ocr.user = request.user
                ocr.text = execute(request.FILES['image'], request.POST['lang'])
                ocr.lang = request.POST['lang']
                ocr.save()
                return redirect(ocr_index)
            else:
                messages.error(request, "Name Already Exists")
                return redirect(ocr_index)
    else:
        return redirect(ocr_index)
  
@login_required(login_url = '/login/')  
def deleteocr(request):
    if request.method == "POST":
        name = request.POST['delete']
        try:
            check = Ocr.objects.filter(image = name)
            # remove image too
            check.delete()
            return redirect(ocr_index)
        except Ocr.DoesNotExist:
            return redirect(ocr_index)
    else:
        pass

@login_required(login_url='/login/')
def image_analytics(request, name = None):    
    try:
        ocr = Ocr.objects.get(name = name)
        return render(request, 'image_analytics.html', {'ocr':ocr})
    except Ocr.DoesNotExist:
        return render(request, '404.html', {"error": "No Such Image Exists."})
