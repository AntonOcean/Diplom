from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserQueryManager(models.Manager):
    def all(self):
        return self.order_by('-id')


class UserQuery(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255, default="")
    title = models.CharField(max_length=255, default="")
    keywords = models.CharField(max_length=255, default="")
    year1 = models.CharField(max_length=4, default="")
    year2 = models.CharField(max_length=4, default="")
    #finish = models.BooleanField(default=False)
    objects = UserQueryManager()

    def get_url(self):
        return "/query_detail/{}/".format(self.timestamp)

    def get_absolute_url(self):
        return reverse('query_detail', kwargs={'timestamp': self.timestamp})

    def __str__(self):
        return self.timestamp

class Document(models.Model):
    user_query = models.ForeignKey(UserQuery, on_delete=models.CASCADE)
    local_url = models.FilePathField(max_length=600)
    net_url = models.URLField(max_length=600)
    title = models.CharField(max_length=200)
    #query_url = models.URLField()

    def __str__(self):
        return self.title

class BaseUrlParser(models.Model):
    user_query = models.ForeignKey(UserQuery, on_delete=models.CASCADE)
    url_cyberleninka = models.URLField(max_length=600)
    url_scholar = models.URLField(max_length=600)
    url_socio = models.URLField(max_length=600)

    def __str__(self):
        return 'Base url #' + str(self.id)
