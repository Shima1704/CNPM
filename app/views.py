from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import * 
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils import timezone
from .models import Order
from . import views
def hoadon(request):
    now = timezone.now()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'now': now}
    return render(request, 'app/hoadon.html', context)
# Create your views here.
def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub = False)
    context={'products':products,'categories':categories,'items':items, 'order' : order, 'cartItems':cartItems,'user_not_login':user_not_login,'user_login': user_login}
    return render(request,'app/detail.html',context)
def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
    context = {'categories':categories,'products':products,'active_category':active_category,'user_not_login':user_not_login,'user_login': user_login}
    return render(request,'app/category.html',context)  
def search(request):
    if request.method=="POST":
        searched =request.POST["searched"]
        keys = Product.objects.filter(name__contains= searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    
    products = Product.objects.all()
    return render(request,'app/search.html', {"searched":searched, "keys":keys, 'products' : products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login': user_login})
def register(request):
    form = CreateUserForm()
    
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')   
    context = {'form':form}
    return render(request,'app/register.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:messages.info(request,'user or password not correct!')

    context = {}
    return render(request,'app/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub =False)
    products = Product.objects.all()
    context={'categories':categories,'products' : products,'cartItems':cartItems, 'user_not_login':user_not_login,'user_login': user_login}
    return render(request,'app/home.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    context={'categories':categories,'items':items, 'order' : order, 'cartItems':cartItems,'user_not_login':user_not_login,'user_login': user_login}
    return render(request,'app/cart.html',context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    context={'items':items, 'order' : order, 'cartItems':cartItems, 'user_not_login':user_not_login,'user_login': user_login}
    return render(request,'app/checkout.html',context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse('added', safe=False)

def checkout_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        mobile = request.POST.get('mobile')
        country = request.POST.get('country')
        total_items = request.POST.get('total_items')  # Lấy từ session/cart logic
        total_price = request.POST.get('total_price')  # Lấy từ session/cart logic

        # Lưu vào database
        order = Order.objects.create(
            name=name,
            email=email,
            address=address,
            city=city,
            state=state,
            mobile=mobile,
            country=country,
            total_items=total_items,
            total_price=total_price,
        )

        return redirect('hoadon')  # Chuyển hướng đến trang hóa đơn hoặc cảm ơn
    else:
        # Render trang checkout với dữ liệu cần thiết (ví dụ: giỏ hàng)
        items = []  # Lấy dữ liệu từ session hoặc database
        order_summary = {
            'total_items': 5,  # Ví dụ
            'total_price': 100000  # Ví dụ
        }
        return render(request, 'checkout.html', {'items': items, 'order': order_summary})