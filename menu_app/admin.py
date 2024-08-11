from django.contrib import admin
from .models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'name', 'parent')
    list_filter = ('parent',)
    search_fields = ('title',)

admin.site.register(MenuItem, MenuItemAdmin)
