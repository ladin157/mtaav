from django.db import models
from django.contrib.auth.models import Permission, User
from django.db import models
import datetime

# Create your models here.

class Category(models.Model):
    # user = models.ForeignKey(User, default=1)
    # artist = models.CharField(max_length=250)
    # album_title = models.CharField(max_length=500)
    # genre = models.CharField(max_length=100)
    # album_logo = models.FileField()
    # is_favorite = models.BooleanField(default=False)

    user = models.ForeignKey(User, default=1)
    provider = models.CharField(max_length=250)
    category_title = models.CharField(max_length=500)
    type = models.CharField(max_length=100)
    category_logo = models.FileField(upload_to=category_title)
    date_created = models.DateField(default=datetime.date.today)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.category_title + ' - ' + self.provider


class File(models.Model):
    # album = models.ForeignKey(Category, on_delete=models.CASCADE)
    # song_title = models.CharField(max_length=250)
    # audio_file = models.FileField(default='')
    # is_favorite = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    filename = models.CharField(max_length=250)
    data_file = models.FileField(default='', upload_to=category)
    date_created = models.DateField(default=datetime.date.today)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.filename
