from django.urls import path
from . import views

urlpatterns = [
    # Restaurant endpoints
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/create/', views.restaurant_create, name='restaurant_create'),
    path('restaurants/<str:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurants/<str:restaurant_id>/dishes/', views.restaurant_dishes, name='restaurant_dishes'),

    # Dish endpoints
    path('dishes/', views.dish_list, name='dish_list'),
    path('dishes/create/', views.dish_create, name='dish_create'),
    path('dishes/<str:dish_id>/', views.dish_detail, name='dish_detail'),
    path('dishes/<str:dish_id>/update/', views.dish_update, name='dish_update'),

    # User endpoints
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<str:user_id>/', views.user_detail, name='user_detail'),
    path('users/<str:user_id>/cart/add/', views.user_add_to_cart, name='user_add_to_cart'),
    path('users/<str:user_id>/payment/', views.user_make_payment, name='user_make_payment'),
    path('users/<str:user_id>/orders/', views.user_orders, name='user_orders'),

    # Order endpoints
    path('orders/', views.order_list, name='order_list'),
    path('orders/<str:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<str:order_id>/send/', views.order_send_for_delivery, name='order_send_for_delivery'),
    path('orders/<str:order_id>/deliver/', views.order_confirm_delivery, name='order_confirm_delivery'),

    # Test endpoint
    path('setup/sample/', views.create_sample_data, name='create_sample_data'),

]
