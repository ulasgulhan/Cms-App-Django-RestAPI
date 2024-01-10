from django.db import models
from django.urls import reverse

# Create your models here.

STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Passive', 'Passive'),
        ('Modified', 'Modified'),
    ]

class Category(models.Model):
    category_name   = models.CharField(max_length=100, unique=True)
    slug            = models.SlugField(max_length=100, unique=True)
    description     = models.TextField(max_length=255)
    status          = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Active')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
    
    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    subcategory_name    = models.CharField(max_length=100, unique=True)
    slug                = models.SlugField(max_length=100, unique=True)
    description         = models.TextField(max_length=255)
    status              = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Active')
    parent_category     = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'
    
    def get_url(self):
        return reverse('products_by_subcategory', args=[self.parent_category.slug, self.slug])
    
    def __str__(self):
        return self.subcategory_name


class Product(models.Model):
    product_name    = models.CharField(max_length=100)
    slug            = models.SlugField(max_length=100, unique=True)
    description     = models.TextField(max_length=1000)
    price           = models.IntegerField()
    image           = models.ImageField(upload_to='photos/product', blank=True)
    stock           = models.IntegerField()
    status          = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Active')
    category        = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subcategory')
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_details', args=[self.category.parent_category.slug, self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class Pages(models.Model):
    page_name       = models.CharField(max_length=20)
    slug            = models.SlugField(max_length=100, unique=True)
    status          = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Active')
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = 'page'
        verbose_name_plural = 'pages'

    def __str__(self):
        return self.page_name

    
