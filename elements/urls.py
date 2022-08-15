from django.urls import path
from .views import product_list, product_detail

app_name = 'elements'

urlpatterns = [
    path('', product_list, name='elements'),
    path('product_detail/<int:product_pk>/', product_detail, name='product_detail'),
]
