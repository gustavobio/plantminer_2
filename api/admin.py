from django.contrib import admin
from .models import Names, ShortNames, Details, Relationships

# Register your models here.

admin.site.register(Details)
admin.site.register(ShortNames)
admin.site.register(Names)
admin.site.register(Relationships)