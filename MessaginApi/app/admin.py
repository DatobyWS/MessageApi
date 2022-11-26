from django.contrib import admin

from .models import MessageUser,Message

admin.site.register(MessageUser)
admin.site.register(Message)