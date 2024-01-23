from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import serializers
from cms.models import Category, Product, SubCategory
from django.contrib.auth.hashers import make_password, check_password



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'last_login']


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        password2 = self.validated_data['password2']

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({"Error": "Email already exists"})
        
        if password2 != self.validated_data['password']:
            raise serializers.ValidationError({'Error': 'Password must match!'})

        user = User.objects.create(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            password=make_password(self.validated_data['password']),
        )
        
        user.save()
        return user