from django.contrib import admin

# Register your models here.
from .models import Member
from .models import Member, CustomToken

admin.site.register(Member)
admin.site.register(CustomToken)

