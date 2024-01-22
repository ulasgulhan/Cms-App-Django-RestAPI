from string import punctuation
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from cms.models import Category, Product, SubCategory



class RegisterForm(UserCreationForm):
    email       = forms.EmailField(required=True)
    first_name  = forms.CharField(required=True)
    last_name   = forms.CharField(required=True)

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class ProductCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=SubCategory.objects.all().order_by('parent_category__category_name'), empty_label="Select a category", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ['product_name', 'image', 'category', 'description', 'price', 'stock']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        self.fields['product_name'].required = True
        self.fields['category'].required = True
        self.fields['image'].required = True
        self.fields['description'].required = True
        self.fields['price'].required = True
        self.fields['stock'].required = True
    
    def clean_title(self):
        product_name = self.cleaned_data.get('product_name')

        for c in product_name:
            if c in punctuation:
                raise forms.ValidationError('Meeting cannot contains punctuation!')

        return product_name

