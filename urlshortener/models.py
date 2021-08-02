from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

MYURL = getattr(settings,'MYURL','https://webify.azurewebsites.net/')

class shorturl(models.Model):
    original_url = models.URLField(blank=False)
    short_url = models.CharField(blank=False, max_length=8)
    date = models.DateField(default=datetime.date.today)
    counter = models.IntegerField(default=0)
    chrome = models.IntegerField(default=0)
    firefox = models.IntegerField(default=0)
    safari = models.IntegerField(default=0)
    other_browser = models.IntegerField(default=0)
    android = models.IntegerField(default=0)
    ios = models.IntegerField(default=0)
    window = models.IntegerField(default=0)
    linux = models.IntegerField(default=0)
    mac = models.IntegerField(default=0)
    other_platform = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_short_url(self):
        url_path = reverse("redirect",kwargs= {'shortcode':self.short_url})
        url_path = MYURL+url_path
        return url_path

    def get_url(self):
        return MYURL