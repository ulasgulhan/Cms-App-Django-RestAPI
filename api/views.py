from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from rest_framework import serializers, permissions
from rest_framework.authentication import authenticate
from rest_framework.decorators import api_view
from api.serializers import CategorySerializer, CreateProductSerializer, SubCategorySerializer, ProductSerializer, UpdateProductSerializer, UserPermissionChangeSerializer, UserPermissionSerializer, UserRegisterSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveUpdateAPIView 
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from cms.models import Category, Product, SubCategory

# Create your views here.


# region Product Lists Views

@method_decorator(login_required(login_url='api_login'), name='dispatch')
class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)


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

# endregion


# region Profile and Dashboard

@method_decorator(login_required(login_url='api_login'), name='dispatch')
class DashboardAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Product.objects.filter(supplier=self.request.user)
            return queryset
        else:
            raise serializers.ValidationError({'Error': 'You must be staff for enter'})



@method_decorator(login_required(login_url='api_login'), name='dispatch')
class ProfileAPIView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(pk=self.request.user.id)
        return queryset

# endregion


# region User Permisson Change 


@method_decorator(login_required(login_url='api_login'), name='dispatch')
class PermissionAPIView(ListAPIView):
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UserPermissionSerializer
    permission_classes = [permissions.IsAdminUser]





@method_decorator(login_required(login_url='api_login'), name='dispatch')
class PermissionChangeAPIView(RetrieveUpdateAPIView):
    serializer_class = UserPermissionChangeSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)
        return user

    
    def get(self, *args, **kwargs):
        user = self.get_queryset()
        serializer = self.get_serializer(instance=user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = self.get_queryset()
        if user.is_staff:
            user.is_staff = False
        else:
            user.is_staff = True
        user.save()
        return redirect('api_permisson')

# endregion


# region Create, Update, Delete

@method_decorator(login_required(login_url='api_login'), name='dispatch')
class ProductCreateAPIView(CreateAPIView):
    serializer_class = CreateProductSerializer
    def save(self, request):
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['supplier'] = request.user
            serializer.save()
            return redirect('product_list')



@method_decorator(login_required(login_url='api_login'), name='dispatch')
class ProductUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UpdateProductSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        if product.supplier != self.request.user:
            return None 
        return product 
    
    def get(self, request, *args, **kwargs):
        product = self.get_queryset()
        if product is None:
            return Response('You cannot change others product', status=403)
        serializer = self.get_serializer(instance=product)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        product = self.get_queryset()
        if product is None:
            return Response('You cannot change others product', status=403)
        serializer = self.get_serializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return redirect('product_list')
    

@method_decorator(login_required(login_url='api_login'), name='dispatch')
class ProductDeleteAPIView(DestroyAPIView):
    serializer_class = UpdateProductSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('pk')
        product = get_object_or_404(Product, id=product_id)
        if product.supplier != self.request.user:
            return None 
        return product 

    
    def get(self, request, *args, **kwargs):
        product = self.get_queryset()
        if product is None:
            return Response('You cannot delete others product', status=403)
        serializer = self.get_serializer(instance=product)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        product = self.get_queryset()
        if product is None:
            return Response('You cannot delete others product', status=403)
        product.status = 'Passive'
        product.save()
        return redirect('product_list')





""" @api_view(['GET', 'POST'])
def update_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, supplier=request.user)
    if request.method == 'POST':
        serializer = UpdateProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return redirect('product_list')
    else:
        serializer = UpdateProductSerializer(instance=product)
        return Response(serializer.data)
 """


# endregion


# region Authentication

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                user = serializer.save()
                data['first_name'] = user.first_name
                data['last_name'] = user.last_name
                data['username'] = user.username
                data['email'] = user.email
                return redirect('product_list')
            except serializers.ValidationError as e:
                data = {'error': e.detail}
        return Response(data)


@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return Response({'detail': 'Logout successful'})


@csrf_exempt
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            return Response({'detail': 'Invalid login credentials'}, status=401)

# endregion


