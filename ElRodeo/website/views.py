from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
import datetime
import json
from django.http import JsonResponse
import random

from .models import *

# Create your views here.

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            return render(request, "website/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "website/login.html")

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)


        if user.exists():
            messages.info(request, "User already exists")
            return redirect('register')

        user = User.objects.create_user(email, password)
        

        messages.info(request, "Account Created Successfully!")
        return redirect('login')
    
    return render(request, "website/register.html")

def logout_view(request):
    logout(request)
    return redirect('login')

def cart(request):
    if request.user.is_authenticated: 
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    return render(request, 'website/cart.html', {
        'items': items,
        'order': order,
        'cartItems': cartItems
    })

def menu(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    meatProducts = Product.objects.filter(category='Meat')
    other = Product.objects.filter(category='Other')
    drinks = Product.objects.filter(category='Drinks')

    return render(request, "website/menu.html", {
        'meatProducts': meatProducts, 
        'other': other, 
        'drinks': drinks,
        'items': items,
        'cartItems': cartItems
    })

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    return render(request, 'website/checkout.html', {
        'items': items,
        'order': order,
        'cartItems': cartItems
    })

def updateItem(request): 
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    quantity = data['quantity']

    print('Action: ', action)
    print('ProductID:', productId)
    print('Quantity: ', quantity)

    customer = request.user
    product = Product.objects.get(name=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + quantity)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - quantity)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def orders(request):
    orders = Order.objects.filter(submitted=True).filter(complete=False)
    list = {}
    for order in orders:
        list[order.customer] = OrderItem.objects.filter(order=order)
        print(order.customer)
    print(list)
    unfulfilled_list = {}
    for key, vals in list.items():
        product_list = {}
        for x in vals:
            product_list[x.product.name] = x.quantity
        unfulfilled_list[key] = product_list

    return render(request, 'website/orders.html', {
        'unfulfilled_list': unfulfilled_list
    })

def order_completed(request):
    data = json.loads(request.body)
    user = User.objects.get(email=data['user'])

    print(user)

    order = Order.objects.filter(customer=user).get(complete=False)
    print(order)
    order.complete = True
    order.save()

    return JsonResponse("successful", safe=False)

def submit_order(request):
    data = json.loads(request.body)
    user = User.objects.get(email=data['customer'])
    order = Order.objects.filter(customer=user).get(submitted=False)

    print(user)
    print(order)
    order.submitted = True
    order.save()

    return JsonResponse("Successful", safe=False)