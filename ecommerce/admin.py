from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin

from .models import *

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display =['name', 'slug', 'parent', 'posted_by', 'created_at','show_image']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"

    # exclude =['posted_by']

    def get_fields(self, request, obj = None):
        fields = []
        if request.user.is_superuser:
            fields.append('posted_by')
        fields.extend(['name', 'slug', 'parent', 'image', 'description', 'meta_title', 'meta_description'])
        return fields
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.posted_by = request.user
        super().save_model(request, obj, form, change)


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(posted_by=request.user)

class AdminMediaInline(admin.TabularInline):
    model = MediaFile
    extra = 5



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'discount_price', 'stock', 'posted_by', 'created_at','show_image']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']
    inlines = [AdminMediaInline]

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"
    



@admin.register(UniqueCart)
class UniqueCartAdmin(admin.ModelAdmin):
    list_display = ['buyer_id', 'total']


