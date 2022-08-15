from django.contrib import admin

from pages.models import Photo, CategoryPhoto


@admin.register(CategoryPhoto)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = [
        'image',
        'category_photo'
    ]
    list_filter = [
        'category_photo'
    ]