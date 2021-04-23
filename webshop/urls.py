from django.urls import include, path
from django.conf.urls import url
from . import views
from .views import (
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    ItemDetailView,
    HomeView,
    add_to_cart,
    remove_from_cart,
)

#app_name= 'webshop'

urlpatterns = [
    path('item_list/', HomeView.as_view(), name='item-list'),
    path('add_to_cart/<int:pk>/',add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>/',remove_from_cart, name='remove_from_cart'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('product/<int:pk>/', ItemDetailView.as_view(), name='product'),
    path('item/new/', PostCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/update/', PostUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', PostDeleteView.as_view(), name='item-delete'),
    path('about/', views.about, name='shop-about'),

]