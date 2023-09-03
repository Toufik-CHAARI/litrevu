from django.contrib import admin
from authentication.models import User


class UserAdmin(admin.ModelAdmin):  # nous insérons ces deux lignes..
    list_display = ('username','first_name', 'last_name')


admin.site.register(User,UserAdmin)