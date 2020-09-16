from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework.mixins import CreateModelMixin
from rest_framework.authentication import TokenAuthentication


from .models import Product, Order, CustomUser
from .serializers import ProductSerializer, OrderSerializer, UserSerializer


# Product List view
class ProductList(generics.ListAPIView):

    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


# Login User view
@csrf_exempt
def loginUserAPI(request):

    if request.method == 'POST':
        
        data = JSONParser().parse(request)
        
        try:
            email = data['email']
            validate_email( email )
        
        except ValidationError:
            return JsonResponse({'Error':'Please enter a valid email'}, status=400)
        
        user = authenticate(request, email=email, password=data['password'])
        
        if user is None:
            try:
                user = CustomUser.objects.create_user(data['email'], password=data['password'])
                user.save()
                token = Token.objects.create(user=user)
                return JsonResponse({'Token':str(token)}, status=201)
            
            except IntegrityError:
                return JsonResponse({'Error':'Incorrect Password, Please try again'}, status=400)
        
        else:
            try:
                token = Token.objects.get(user=user)
            
            except:
                token = Token.objects.create(user=user)
            
            return JsonResponse({'Token':str(token)}, status=201)
    
    else:
        return JsonResponse({'Error':'Bad Request'}, status=400)


# Login Cient
def loginUserView(request):

    user = request.user 

    if request.user.is_authenticated:

        if Token.objects.filter(user=user).exists():
            token = Token.objects.get(user=user)
            return render(request, 'sociallogin.html', {'Token':str(token)})

        else:
            token = Token.objects.create(user=user)
            return render(request, 'sociallogin.html', {'Token':str(token)})

    else:
        return redirect('http://127.0.0.1:8000/accounts/login')
        

# Profile view
class Profile(generics.RetrieveUpdateAPIView, CreateModelMixin):

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):

        user = self.request.user
        return CustomUser.objects.get(pk=user.id)


# Orders view
class OrderList(generics.ListCreateAPIView):

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        user = self.request.user
        return Order.objects.filter(user=user.id)

    def create(self, request, *args, **kwargs):

        if request.method == 'POST':
            
            data = JSONParser().parse(request)
            user = request.user

            for product in data['order'].keys():

                if Product.objects.filter(pk=int(product)).exists():

                    prod = Product.objects.get(pk=int(product))
                    quant = int(data['order'][product])
                    
                    if type(int(product)) != int:
                        return JsonResponse({'Error':'Please enter correct values'}, status=400)
                    
                    if type(quant) != int:
                        return JsonResponse({'Error':'Please enter correct values'}, status=400)
                    
                    if prod.stock == 0:
                        return JsonResponse({'Error':f'Product {product} is not available!'}, status=400)
                    
                    elif prod.stock < quant:
                        return JsonResponse({'Error':f'We don\' have Product {product} enough, srry!'}, status=400)
                    
                    elif prod.stock >= quant:
                        
                        if quant <= 0:
                            return JsonResponse({'Error':'Please enter correct values'}, status=400)
                        else:
                            order = Order(user= user, product= prod, quantity= quant)
                            order.save()
                            prod.stock -= quant
                            prod.save()
                
                else:
                    return JsonResponse({'Error':f'{product} does not exist'}, status=400)    

        if request.method != 'POST':
            return JsonResponse({'Error':'Bad Request'}, status=400)

        return JsonResponse({'Success':'Thank you for buying'}, status=200)        