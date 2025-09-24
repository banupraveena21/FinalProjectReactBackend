from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('cart/', views.CartItemListView.as_view(), name='cart-list'),
    path('cart/add/', views.CartAddView.as_view(), name='cart-add'),
    path('cart/remove/<int:pk>/', views.CartItemRemoveView.as_view(), name='cart-remove'),
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order-create'),
]
