from rest_framework.viewsets import ModelViewSet
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer
from . import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import itertools as it
from django.db import transaction
from profiles_api.models import User
from django_shopper.errors import errors


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(available=True)
    permission_classes = (permissions.AdminUpdateProduct,)


@api_view(['POST'])  # product ordering work with post method
def ordering(request):
    """this method for ordering products=>format of products is:
    {
    "products": [
        {
            "id": 1,
            "count": 1
        }
    ]
}
    """
    # check the format of products
    exceptions = []
    if 'products' not in request.data or type(request.data['products']) != list or len(request.data['products']) == 0:
        code = 100
        error = {
            'code': code,
            'msg': errors[code]
        }
        return Response(error, status.HTTP_400_BAD_REQUEST)
    user_id = request.user.id
    customer = User.objects.get(pk=user_id)  # get instance of login_user
    products_input = request.data['products']  # get products from input
    keyfunc = lambda x: x['id']
    groups = it.groupby(products_input, keyfunc)  # it is possible the user input same id,with group delete duplicate and sum count of them
    try:
        # {"products": [{"id": 1,"count": 1},{"id": 1,"count": 5},{"id": 2,"count": 3}]}==>convert to
        # {"products": [{"id": 1,"count": 6},{"id": 2,"count": 3}]}
        products_input = [{'id': k, 'count': sum(x['count'] for x in g)} for k, g in groups]
    except:
        code = 100
        error = {
            'code': code,
            'msg': errors[code]
        }
        return Response(error, status.HTTP_400_BAD_REQUEST)
    try:

        with transaction.atomic():  # with attomic happen roll back ...if happen error in forloop ...The order and orderitem will not be registered
            order = Order(customer_id=customer)
            order.save()
            for product in products_input:
                product_obj = ''
                try:
                    product_obj = Product.objects.get(pk=product['id'])  # get instance of Product
                except:
                    code = 101
                    error = {
                        'code': code,
                        'msg': errors[code]
                    }
                    exceptions.append({
                        'id': product['id'],
                        'error': error,
                    })
                if product['count'] > 0:
                    if product_obj == '':
                        pass
                    else:

                        if product_obj.check_remaind_count(product['count']):  # check remaind_count of product before register order
                            order_item = OrderItem(order_id=order, product_id=product_obj, count=product['count'])
                            order_item.save()
                        else:
                            code = 103
                            error = {
                                'code': code,
                                'msg': errors[code]
                            }
                            exceptions.append({
                                'id': product['id'],
                                'error': error
                            })
                else:
                    # count of product can not 0 or negative number
                    code = 102
                    error = {
                        'code': code,
                        'msg': errors[code]
                    }
                    exceptions.append({
                        'id': product['id'],
                        'error': error
                    })

            # raise exception handly to trigger rollback
            if len(exceptions) > 0:
                # raise ("raise for rollback")
                transaction.set_rollback(True)  # if length of exception is greather than zero run rollback
                return Response(exceptions, status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        pass
    res = {'پیغام': 'سفارش شما با موفقیت ثبت شد.'}

    return Response(res, status.HTTP_200_OK)
