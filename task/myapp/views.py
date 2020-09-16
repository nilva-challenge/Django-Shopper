from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from myapp.models import Product, Order
from myapp.serializers import ProductSerializer


# ApiLogin create(if user does not exist) or authenticate the user  and creating token after that.
@csrf_exempt
def ApiLogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        result = User.objects.filter(email=email).first()
        if result is None:
            result = email.split("@")[0]
            temp = User.objects.create_user(result, email, password)
            temp.save()

        user = authenticate(username=result, password=password)

        if user is not None:
            token, create = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key})
        else:
            return JsonResponse({'auth': 'False'})


# profile GET first name & last name + POST and update first name & last name
@api_view(['GET', 'POST'])
def ApiProfile(request):
    if request.method == 'GET':
        return Response(
            {"username": str(request.user), "Name": str(request.user.first_name) + str(request.user.last_name)})
    # we can use a dictionary something like **kwargs for handling more variables but in this simple case these two if
    # statements are enough.
    if request.method == 'POST':
        update_user = User.objects.get(username=str(request.user))
        if 'first_name' in request.POST:
            update_user.first_name = request.POST['first_name']
        if 'last_name' in request.POST:
            update_user.last_name = request.POST['last_name']
        update_user.save()
        return Response({'response': 'updated'})


@api_view(['GET'])
def ApiProduct(request):
    product_query = Product.objects.exclude(available=0)
    serializer = ProductSerializer(product_query, many=True)
    return Response(serializer.data)


# define default count as 1 but reassign whenever need;creating orders using POST.
@api_view(['POST'])
def ApiOrder(request):
    user_obj = request.user
    count = 0  # default parameter
    if 'count' in request.POST: # data validation
        count = int(request.POST['count'])
    if 'product_id' in request.POST:
        product_id = request.POST['product_id']
        try:
            product_query = Product.objects.get(id=product_id)
        except Product.DoesNotExist:  # bad request; could be 400 but wanna explain more about that.
            return Response({'error': 'probably problem in product id parameter'})
        product_availability = int(product_query.available)
        if count <= product_availability:

            new_order = Order.objects.create(user_fk=user_obj, product_fk=product_query, count=count)
            new_order.save()
            product_query.available = int(product_availability - count)
            product_query.save()
            return Response({'response': 'order' + product_id + 'has been successfully created'})
        else:
            return Response({'error': 'probably problem in count parameter'})
    else:  # more like bad request again but explaining more details in json instead of raising error number.(400.6)
        return Response({'error': 'probably problem in product id parameter'})
