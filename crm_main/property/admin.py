
# Register your models here.
from django.contrib import admin
from .models import Property, PropertyImage, PropertyComment, PropertyCommentImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class PropertyCommentImageInline(admin.TabularInline):
    model = PropertyCommentImage
    extra = 1

class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]

class PropertyCommentAdmin(admin.ModelAdmin):
    inlines = [PropertyCommentImageInline]

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyComment, PropertyCommentAdmin)

