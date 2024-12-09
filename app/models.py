from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Category model
class Category(models.Model):
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True
    )
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


# Custom user creation form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


# Product model
class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='product')
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True, default='default.jpg')  # Cung cấp ảnh mặc định
    detail = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = '/static/default.jpg'  # Đường dẫn tới ảnh mặc định
        return url


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"Order #{self.id} - {'Complete' if self.complete else 'Incomplete'}"

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# ShippingAddress model
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=100, null=True)  # Không cần blank=True, vì có thể không cần yêu cầu country trống
    mobile = models.CharField(max_length=15, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.country}"

# ShippingAddress form
class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'country', 'mobile']
        
        # Thiết lập các nhãn cho các trường
        labels = {
            'address': 'Địa chỉ',
            'city': 'Thành phố',
            'state': 'Tỉnh/Thành phố',
            'country': 'Quốc gia',
            'mobile': 'Số điện thoại',
        }

        # Thiết lập thuộc tính widget để tùy chỉnh kiểu input
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập địa chỉ của bạn'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập thành phố'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tỉnh/thành phố'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập quốc gia'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số điện thoại'}),
        }

        # Thiết lập trường required cho các trường
        required = {
            'address': True,
            'city': True,
            'state': True,
            'country': True,
            'mobile': True,
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if len(mobile) < 10:
            raise forms.ValidationError("Số điện thoại phải có ít nhất 10 ký tự.")
        return mobile
