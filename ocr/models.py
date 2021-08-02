import datetime
from django.db import models
from django.contrib.auth.models import User

class Ocr(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    lang = models.CharField(max_length=5)
    image = models.ImageField(upload_to="images/", verbose_name="Input Image")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)

    class Meta:
        ordering = ('-name',)