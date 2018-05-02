from django.contrib import admin

from .models import UserQuery, Document, BaseUrlParser, Tags

admin.site.register(UserQuery)
admin.site.register(Document)
admin.site.register(BaseUrlParser)
admin.site.register(Tags)
