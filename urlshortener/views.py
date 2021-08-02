from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from .models import shorturl
from .utils import shortcode
import random
from django.http import HttpResponseRedirect

def error_404_view(request, exception):
    return render(request, '404.html')

@login_required(login_url = '/login/')
def shorty(request):
    user = request.user
    url = shorturl.objects.filter(user = user)
    url_paginator = Paginator(url, 7)
    urls = request.GET.get('page')
    try:
        url_1 = url_paginator.page(urls)
    except PageNotAnInteger:
        url_1 = url_paginator.page(1)
    except EmptyPage:
        url_1 = url_paginator.page(url_paginator.num_pages)
    return render(request, 'shorty.html', {'urls':url_1})

@login_required(login_url= '/login')
def generate(request):
    if request.method == "POST":
        if request.POST['original']:
            user = request.user
            original = request.POST['original']
            if not shorturl.objects.filter(original_url = original, user = user).exists():
                url_generated = False
                short_code = shortcode(original)
                while not url_generated:
                    check = shorturl.objects.filter(short_url = short_code)
                    if not check:
                        newurl = shorturl(
                            user = user,
                            original_url = original,
                            short_url = short_code,
                        )
                        newurl.save()
                        return redirect('/shorty')
                    else:
                        short_code = ''.join(random.sample(short_code, len(short_code)))
            else:
                messages.error(request, "URL Already Exists")
                return redirect(shorty)
        else:
            messages.error(request, "Empty Fields")
            return redirect(shorty)
    else:
        return redirect(shorty)

@login_required(login_url='/login/')
def deleteurl(request):
    if request.method == "POST":
        short = request.POST['delete']
        try:
            check = shorturl.objects.filter(short_url=short)
            check.delete()
            return redirect(shorty)
        except shorturl.DoesNotExist:
            return redirect(shorty)
    else:
        return render(request, '404.html', {"error" : "No Such URL Exists to Delete"})

@login_required(login_url='/login/')
def analytics(request, short_code = None):    
    try:
        url = shorturl.objects.get(short_url = short_code)
        return render(request, 'analytics.html', {'url':url})
    except shorturl.DoesNotExist:
        return render(request, '404.html', {"error": "No Analytics Data for Such URL."})

def redirectView(request, shortcode=None):
    if not shortcode or shortcode is None:
        return render(request, 'index.html')
    else:
        platform = request.user_agent.os.family
        browser = request.user_agent.browser.family
        browser_dict = {'Firefox': 0 , 'Chrome':0 , 'Mobile Safari':0 , 'other_browser':0}
        platform_dict = {'Windows':0 , 'iOS':0 , 'Android':0 , 'Linux':0 , 'MAC':0 , 'other_platform':0}
        if browser in browser_dict:
            browser_dict[browser] += 1
        else:
            browser_dict['other_browser'] += 1
        if platform in platform_dict:
            platform_dict[platform] += 1
        else:
            platform_dict['other_platform'] += 1
        try:
            obj = shorturl.objects.get(short_url=shortcode)
            obj.counter += 1
            obj.chrome += browser_dict['Chrome']
            obj.firefox += browser_dict['Firefox']
            obj.safari += browser_dict['Mobile Safari']
            obj.other_browser += browser_dict['other_browser']
            obj.android += platform_dict['Android']
            obj.ios += platform_dict['iOS']
            obj.window += platform_dict['Windows']
            obj.linux += platform_dict['Linux']
            obj.mac += platform_dict['MAC']
            obj.other_platform += platform_dict['other_platform']
            obj.save()
            return HttpResponseRedirect(obj.original_url)
        except shorturl.DoesNotExist:
            #messages.add_message(request, messages.ERROR, 'URL Does not exist')
            return render(request, '404.html', {"msg": "No such Short URL exists."})