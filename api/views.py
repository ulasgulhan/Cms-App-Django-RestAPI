from unicodedata import category
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import response, views
from api.serializers import CategorySerializer, SubCategorySerializer, ProductSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView

from cms.models import Category, Product, SubCategory

# Create your views here.


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryListAPIView(ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ProductByCategoryListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        parent_category = get_object_or_404(Category, slug=category_slug)
        subcategory = SubCategory.objects.filter(parent_category=parent_category)
        queryset = Product.objects.filter(category__in=subcategory)
        return queryset


class ProductBySubCategoryListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        subcategory_slug = self.kwargs['subcategory_slug']
        queryset = Product.objects.filter(category__parent_category__slug=category_slug, category__slug=subcategory_slug)
        return queryset


class ProductDetailAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        subcategory_slug = self.kwargs['subcategory_slug']
        product_slug = self.kwargs['product_slug']
        queryset = Product.objects.filter(category__parent_category__slug=category_slug, category__slug=subcategory_slug, slug=product_slug)
        return queryset