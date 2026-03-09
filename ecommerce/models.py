from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Category(MPTTModel):
    posted_by = models.ForeignKey(User, on_delete=models.PROTECT)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    description = RichTextField(blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name_plural = 'Category'


    def child(self):
        return Category.objects.filter(parent=self)

  



class Product(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    description = RichTextField(blank=True)    
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class MediaFile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='product_media/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media for {self.product.name}"
    


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

