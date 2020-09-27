from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
import json
import datetime
from .models import *
from .utils import cartData, guestOrder


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('store')
    template_name = 'signup.html'


@login_required
def profile(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            context = User.objects.get(id=request.user.id)
            return render(request, context)


@login_required
def store(request):
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        # order = data['order']
        # items = data['items']
        products = Product.objects.all()
        context = {'products': products, 'cartItems': cartItems}
        return render(request, 'store/store.html', context)
    else:
        return HttpResponse(status=401)


@login_required
def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


@login_required
def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


@login_required
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

@login_required
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city']
        )

    return JsonResponse('Payment submitted..', safe=False)
