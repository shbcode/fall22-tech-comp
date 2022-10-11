from multiprocessing import context
from re import A
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from account import ACCOUNT
from .models import *

# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/store.html', context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, fulfilled = False)
        items = order.orderedproduct_set.all()
    else:
        items = []
        order = {"get_cart_total":0, "get_cart_items":0, 'shipping':False}

    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, fulfilled = False)
        items = order.orderedproduct_set.all()
    else:
        items = []
        order = {"get_cart_total":0, "get_cart_items":0, 'shipping':False}

    context = {'items':items, 'order':order}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    # return JsonResponse("Item was properly added", safe = False)
    data = json.loads(request.body)
    action = data['action']
    productId = data['productId']
    print("Action: ", action)
    print("Product: ", productId)
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, fulfilled = False)
    orderItem, created = orderedproduct.objects.get_or_create(order=order,product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, fulfilled=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.get_cart_total:
            order.fulfilled = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in')

    return JsonResponse('Payment submitted...', safe=False)