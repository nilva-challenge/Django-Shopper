from django.urls import path, include
from . import views

urlpatterns = [


    path('all_products', views.show_products_list, name='show_products_list'),
    path('new_order', views.new_order, name='new_order'),

]
