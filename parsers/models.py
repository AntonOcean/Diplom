from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserQueryManager(models.Manager):
    def all(self):
        return self.order_by('-id')


class Tags(models.Model):
    name_tag = models.CharField(max_length=255)


class UserQuery(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255, default="")
    title = models.CharField(max_length=255, default="")
    keywords = models.CharField(max_length=255, default="")
    year1 = models.CharField(max_length=4, default="")
    year2 = models.CharField(max_length=4, default="")
    tags = models.ManyToManyField(Tags)
    objects = UserQueryManager()

    def get_url(self):
        return "/query_detail/{}/".format(self.timestamp)

    def get_absolute_url(self):
        return reverse('query_detail', kwargs={'timestamp': self.timestamp})

    def get_date(self):
        date = self.timestamp.split('-')
        date_line = date[2] + '.' + date[1] + '.' + date[0] + ' в ' + date[3] + ':' + date[4]
        if not self.user:
            user = 'Anonymous'
        else:
            user = self.user
        return 'Запрос от {} выполнен {}'.format(str(user), date_line)

    def get_name(self):
        date = self.timestamp.split('-')
        date_line = date[2] + '.' + date[1] + '.' + date[0] + ' в ' + date[3] + ':' + date[4]
        if not self.user:
            user = 'Anonymous'
        else:
            user = self.user
        return '{}: {}'.format(str(user), date_line)

    def keywords_to_socionet(self):
        if self.title:
            return self.title + ' ' + self.keywords
        return self.keywords

    def __str__(self):
        return self.timestamp


class Document(models.Model):
    user_query = models.ForeignKey(UserQuery, on_delete=models.CASCADE)
    local_url = models.FilePathField(max_length=600)
    net_url = models.URLField(max_length=600)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class BaseUrlParser(models.Model):
    user_query = models.ForeignKey(UserQuery, on_delete=models.CASCADE)
    url_cyberleninka = models.URLField(max_length=600)
    url_scholar = models.URLField(max_length=600)
    url_socio = models.URLField(max_length=600)

    def __str__(self):
        return 'Base url #' + str(self.id)
