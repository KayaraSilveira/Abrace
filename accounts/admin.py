from django.contrib import admin
from .models import CustomUser, Category

class CustomUserAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
