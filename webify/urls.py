"""webify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentication import views
from ocr.views import convert, ocr_index, deleteocr, image_analytics
from urlshortener.views import shorty, generate, deleteurl, analytics, redirectView
from django.conf.urls import handler404, url

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('ocr/', ocr_index, name = 'ocr_index'),
    path('convert/', convert, name = 'convert'),
    path('login/', views.login, name = "login"),
    path('signup/', views.signup, name = "signup"),
    path('logout/', views.logout, name = "logout"),
    path('shorty/', shorty, name = "shorty"),
    path('generate/', generate, name = "generate"),
    path('deleteocr/', deleteocr, name = 'deleteocr'),
    path('deleteurl/', deleteurl, name="deleteurl"),
    path('image_analytics/<str:name>', image_analytics, name="image_analytics"),
    path('analytics/<str:short_code>', analytics, name="analytics"),
    url(r'^(?P<shortcode>[\w-]+)/$', redirectView, name='redirect'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'authentication.views.error_404_view'
handler404 = 'urlshortener.views.error_404_view'