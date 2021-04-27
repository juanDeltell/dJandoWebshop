from django.urls import include, path
from django.conf.urls import url
from . import views
from . import forms
from .views import (
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    ItemDetailView,
    HomeView,
    HomeViewShortedByHighPrice,
    HomeViewShortedByLowPrice,
    HomeViewShortedByAName,
    HomeViewShortedByZName,
    add_to_cart,
    remove_from_cart,
    OrderSummaryView,
    CheckoutView,
    remove_single_item_from_cart,
)

#app_name= 'webshop'

urlpatterns = [
    path('item_list/', HomeView.as_view(), name='item_list'),
    path('HomeViewShortedByHighPrice/', HomeViewShortedByHighPrice.as_view(), name='HomeViewShortedByHighPrice'),
    path('HomeViewShortedByLowPrice/', HomeViewShortedByLowPrice.as_view(), name='HomeViewShortedByLowPrice'),
    path('HomeViewShortedByAName/', HomeViewShortedByAName.as_view(), name='HomeViewShortedByAName'),
    path('HomeViewShortedByZName/', HomeViewShortedByZName.as_view(), name='HomeViewShortedByZName'),
    path('add_to_cart/<int:pk>/',add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>/',remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/<int:pk>/',remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/',OrderSummaryView.as_view(), name='order-summary'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('product/<int:pk>/', ItemDetailView.as_view(), name='product'),
    path('item/new/', PostCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/update/', PostUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', PostDeleteView.as_view(), name='item-delete'),
    path('about/', views.about, name='shop-about'),

]