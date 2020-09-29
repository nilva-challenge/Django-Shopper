from django.shortcuts import render

# Create your views here.
from DjangoShopper.decorators import token_required
from .models import Product, Order, OrderProductRelation
from django.http import JsonResponse
import json
from json import JSONEncoder
from users.models import User


# show all products
@token_required
def show_products_list(request, token):
    products = Product.objects.all().values('id', 'name', 'stock', 'price')
    return JsonResponse(list(products), safe=False)


# create an order by send a list
@token_required
def new_order(request, token):
    order_list = json.loads(request.body)
    id_list = []
    orders = []
    products = []
    for i in order_list:
        id_list.append(i["id"])
        p = Product.objects.get(id=i["id"])
        if p.stock <= i["order_number"]:
            return JsonResponse(
                {'status': 'error',
                 'product_name': p.name,
                 'product_stock': p.stock,
                 'type': 'NotEnoughInventory',
                 }, encoder=JSONEncoder)
        ordered_product = {}
        ordered_product['id'] = p.id
        ordered_product['name'] = p.name
        ordered_product["order_number"] = i["order_number"]
        ordered_product['end_price'] = i["order_number"] * p.price
        ordered_product['unit_price'] = p.price
        p.stock = p.stock - i["order_number"]
        products.append(p)
        orders.append(ordered_product)
    user = User.objects.get(token=token)
    for i in products:
        i.save()
    order = Order.objects.create(user=user)
    for i in orders:
        OrderProductRelation.objects.create(order=order, product_id=i['id'], unit=i['unit_price'],
                                            order_number=i["order_number"])
    return JsonResponse(orders, safe=False)
