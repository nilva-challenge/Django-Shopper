from django.urls import path
from shop import views

app_name = 'shop-api'

urlpatterns = [
    path('item/list/', views.ItemListView.as_view(), name='list-item'),
    path('order/create_list/', views.OrderListCreateView.as_view(), name='list-create-order'),
]
