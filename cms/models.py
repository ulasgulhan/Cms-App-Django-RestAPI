from telnetlib import STATUS
from django.contrib.auth.models import User
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
    subcategory_name    = models.CharField(max_length=100)
    slug                = models.SlugField(max_length=100)
    description         = models.TextField(max_length=255)
    status              = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Active')
    parent_category     = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'
    
    def get_url(self):
        return reverse('products_by_subcategory', args=[self.parent_category.slug, self.slug])
    
    def __str__(self):
        return self.parent_category.category_name + ' >' + self.subcategory_name 


class Product(models.Model):
    product_name    = models.CharField(max_length=100, unique=True)
    slug            = models.SlugField(max_length=100, unique=True)
    description     = models.TextField(max_length=1000)
    price           = models.IntegerField()
    image           = models.ImageField(upload_to='photos/product')
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


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', status='Active')
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', status='Active')


variation_choies = (
    ('color', 'color'),
    ('size', 'size')
)


class Variations(models.Model):
    product_name        = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category  = models.CharField(max_length=100, choices=variation_choies)
    variation_value     = models.CharField(max_length=100)
    status              = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Active')

    objects             = VariationManager()

    class Meta:
        verbose_name = 'variation'
        verbose_name_plural = 'variations'

    def __str__(self):
        return self.variation_value


class Cart(models.Model):
    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    products            = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f'Cart for {self.user}'


class CartItem(models.Model):
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart                = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity            = models.PositiveIntegerField(default=1)
    variation           = models.ManyToManyField(Variations, blank=True)
    status              = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Active')

    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.product.product_name

    
