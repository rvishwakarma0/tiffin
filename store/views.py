from django.shortcuts import render,redirect
from django.http import JsonResponse 
import json
import datetime
from .models import * 
from .utils import CookieCart,cartData, guestOrder
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def store(request):
    
    data = cartData(request)
    items = data['items']
   
    cart_items = data['cart_items']

    products = Product.objects.all() 

    context = {'products':products, 'cart_items':cart_items}
    return render(request, "store/store.html", context)
    



def cart(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']

    context = {'items':items, 'order': order, 'cart_items':cart_items}
    return render(request, "store/cart.html", context)




def checkout(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    context = {'items':items, 'order': order, 'cart_items':cart_items}
    return render(request, "store/checkout.html", context)


def UpdateItem(request):
    data = json.loads(request.body)
    ProductId = data['ProductId']
    action = data['action']
    print('Action:',action)
    print('ProductID:',ProductId)

    customer = request.user.customer
    product = Product.objects.get(id=ProductId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem , created= OrderItem.objects.get_or_create(order=order, product=product)

    if action  == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)


def ProcessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer,order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer= customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
    return JsonResponse('Payment Completed', safe=False)

@login_required
def userLogout(request):
    logout(request)
    return redirect('/')


def loginOrRegister(request):
    data = cartData(request)
    cart_items = data['cart_items']

    if request.method == 'POST':
        
        formType = request.POST.get('formType')
        if formType == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(username=email, password=password)
            if user:
                login(request,user)
                return redirect('/')
            else:
                return render(request,'store/login.html',{'error_msg':'Invalid login details given.', 'cart_items':cart_items})
        elif formType == 'register':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            try:
                user = User.objects.get(username=email)
                return render(request,'store/login.html',{'error_msg_reg':'User already exist, proceed with login or use diffrent email id', 'cart_items':cart_items})
            except:
                user = User.objects.create(username=email)
                user.set_password(password)
                user.save()
                customer, created= Customer.objects.get_or_create(email=email)
                customer.user = user
                customer.name = name
                customer.save()
                return render(request,'store/login.html',{'error_msg_reg':'Successfully registered, Login Now!', 'cart_items':cart_items})


    return render(request, 'store/login.html',{'cart_items':cart_items})


def vendor(request, vid):
    data = cartData(request)
    cart_items = data['cart_items']
    try:
        vendorObj = Vendor.objects.get(id=vid)
    except:
        return redirect('/')
    #products = Product.objects.filter(vendor=vendorObj)
    products = vendorObj.product_set.all()
    print(products)
    context = {
        'cart_items': cart_items,
        'products': products,
        'vendor': vendorObj
    }
    return render(request, 'store/vendor.html', context)


def myOrders():
    return None