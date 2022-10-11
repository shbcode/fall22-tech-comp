from multiprocessing import context
from re import A
from django.shortcuts import render
from django.http import JsonResponse
import json
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
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderedproduct_set.all()
    else:
        items = []
        order = {"get_cart_total":0, "get_cart_items":0, 'shipping':False}

    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
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
    order, created = Order.objects.get_or_create(customer=customer)
    orderItem, created = orderedproduct.objects.get_or_create(order=order,product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)