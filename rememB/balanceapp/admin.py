from django.contrib import admin

from .models import Answer, Balance, Question

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Balance)
