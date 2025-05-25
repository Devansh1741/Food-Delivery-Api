from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Restaurant, Dish, User, Order
import json
import uuid


# helper function to convert output data to json 
def restaurant_to_json(restaurant):
    return {
        'restaurant_id': restaurant.restaurant_id,
        'name': restaurant.name,
        'address': restaurant.address,
    }

def dish_to_json(dish):
    return {
        'dish_id': dish.dish_id,
        'restaurant_id': dish.restaurant_id.restaurant_id, 
        'name': dish.name,
        'price': dish.price,
        'description': dish.description,
        'is_available': dish.is_available,
    }

def user_to_json(user):
    return {
        'user_id': user.user_id,
        'name': user.name,
        'phone_number': user.phone_number,
    }

def order_to_json(order):
    return {
        'order_id': order.order_id,
        'user_id': order.user.user_id, 
        'restaurant_id': order.restaurant_id.restaurant_id, 
        'total_amount': order.total_amount,
        'payment_type': order.payment_type,
        'status': order.status,
        'items': [dish_to_json(item) for item in order.items.all()],
    }


# restaurant apis
@csrf_exempt
@require_GET
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    data = [restaurant_to_json(r) for r in restaurants]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_POST
def restaurant_create(request):
    try:
        data = json.loads(request.body)
        restaurant = Restaurant.objects.create(
            restaurant_id=str(uuid.uuid4()),
            name=data['name'],
            address=data['address']
        )
        return JsonResponse(restaurant_to_json(restaurant), status=201)
    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {e}'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_GET
def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    return JsonResponse(restaurant_to_json(restaurant))


@csrf_exempt
@require_GET
def restaurant_dishes(request, restaurant_id):
    # Get restaurant then their dishes
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    dishes = Dish.objects.filter(restaurant_id=restaurant)
    data = [dish_to_json(d) for d in dishes]
    return JsonResponse(data, safe=False)


# Dishes Apis

@csrf_exempt
@require_GET
def dish_list(request):
    dishes = Dish.objects.all()
    data = [dish_to_json(d) for d in dishes]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_POST
def dish_create(request):
    try:
        data = json.loads(request.body)
        restaurant_obj = get_object_or_404(Restaurant, restaurant_id=data['restaurant_id'])

        dish = Dish.objects.create(
            dish_id=str(uuid.uuid4()),
            restaurant_id=restaurant_obj, 
            name=data['name'],
            price=data['price'],
            description=data.get('description', ''),
            is_available=data.get('is_available', True) 
        )

        return JsonResponse(dish_to_json(dish), status=201)
    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {e}'}, status=400)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant not found'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_GET
def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, dish_id=dish_id)
    return JsonResponse(dish_to_json(dish))

@csrf_exempt
@require_http_methods(["PUT"])
def dish_update(request, dish_id):
    dish = get_object_or_404(Dish, dish_id=dish_id)
    try:
        data = json.loads(request.body)
        dish.name = data.get('name', dish.name)
        dish.price = data.get('price', dish.price)
        dish.description = data.get('description', dish.description)
        dish.is_available = data.get('is_available', dish.is_available)
        dish.save()
        return JsonResponse(dish_to_json(dish))
    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {e}'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

# User apis

@csrf_exempt
@require_GET
def user_list(request):
    users = User.objects.all()
    data = [user_to_json(u) for u in users]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_POST
def user_create(request):
    try:
        data = json.loads(request.body)
        user = User.objects.create(
            user_id=str(uuid.uuid4()),
            name=data['name'],
            phone_number=data['phone_number']
        )
        return JsonResponse(user_to_json(user), status=201)
    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {e}'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_GET
def user_detail(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    return JsonResponse(user_to_json(user))


# Not storing users dishes to cart
# Mock function to simulate it
# For now user need the manually send the dishes ids

@csrf_exempt
@require_POST
def user_add_to_cart(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    try:
        data = json.loads(request.body)
        dish_id = data.get('dish_id')
        if not dish_id:
            return JsonResponse({"error": "dish_id is required"}, status=400)

        dish = get_object_or_404(Dish, dish_id=dish_id)
        return JsonResponse(dish_to_json(dish), status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Dish.DoesNotExist:
        return JsonResponse({"error": "Dish not found"}, status=404)

@csrf_exempt
@require_POST
def user_make_payment(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    try:
        data = json.loads(request.body)
        restaurant_id = data.get('restaurant_id')
        dish_ids = data.get('dish_ids')
        payment_type = data.get('payment_type')

        if not restaurant_id or not dish_ids or not payment_type:
            return JsonResponse({"error": "restaurant_id, dish_ids, and payment_type are required"}, status=400)

        restaurant_obj = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        dishes = Dish.objects.filter(dish_id__in=dish_ids, restaurant_id=restaurant_obj)

        if len(dishes) != len(dish_ids):
            return JsonResponse({"error": "One or more dishes not found in this restaurant"}, status=400)

        total_amount = sum(dish.price for dish in dishes)

        # Create a new order
        order = Order.objects.create(
            order_id=str(uuid.uuid4()),
            user=user,
            restaurant_id=restaurant_obj,
            total_amount=total_amount,
            payment_type=payment_type
        )
        order.items.set(dishes)
        return JsonResponse(order_to_json(order), status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Restaurant.DoesNotExist:
        return JsonResponse({"error": "Restaurant not found"}, status=404)
    except Dish.DoesNotExist:
        return JsonResponse({"error": "One or more dishes not found"}, status=404)
    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {e}'}, status=400)

@csrf_exempt
@require_GET
def user_orders(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    orders = Order.objects.filter(user=user)
    data = [order_to_json(o) for o in orders]
    return JsonResponse(data, safe=False)

# Orders Api

@csrf_exempt
@require_GET
def order_list(request):
    orders = Order.objects.all()
    data = [order_to_json(o) for o in orders]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_GET
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return JsonResponse(order_to_json(order))

@csrf_exempt
@require_POST
def order_send_for_delivery(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    if order.status != 'preparing':
        return JsonResponse({"error": "Order cannot be sent for delivery in the current status."}, status=400)
    order.status = 'delivering'
    order.save()
    return JsonResponse(order_to_json(order))

@csrf_exempt
@require_POST
def order_confirm_delivery(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    if order.status != 'delivering':
        return JsonResponse({"error": "Order cannot be marked as delivered in the current status."}, status=400)
    order.status = 'delivered'
    order.save()
    return JsonResponse(order_to_json(order))



# Helper api to create mock data for testing the apis

@csrf_exempt
@require_POST
def create_sample_data(request):
    try:
        # Create a sample restaurant
        restaurant = Restaurant.objects.create(
            restaurant_id=str(uuid.uuid4()),
            name="Testaurant",
            address="123 Sample Street"
        )

        # Create a sample user
        user = User.objects.create(
            user_id=str(uuid.uuid4()),
            name="John Doe",
            phone_number="1234567890"
        )

        # Create sample dishes
        dish1 = Dish.objects.create(
            dish_id=str(uuid.uuid4()),
            restaurant_id=restaurant,
            name="Spaghetti",
            price=12.99,
            description="Classic Italian pasta",
            is_available=True
        )

        dish2 = Dish.objects.create(
            dish_id=str(uuid.uuid4()),
            restaurant_id=restaurant,
            name="Pizza",
            price=9.99,
            description="Cheesy pepperoni pizza",
            is_available=True
        )

        base_url = request.build_absolute_uri('/')[:-1] 

        return JsonResponse({
            "message": "Sample data created successfully",

            "data": {
                "restaurant": restaurant_to_json(restaurant),
                "user": user_to_json(user),
                "dishes": [dish_to_json(dish1), dish_to_json(dish2)],
            },

            "next_steps": {
                "make_order": {
                    "method": "POST",
                    "url": f"{base_url}/api/users/{user.user_id}/payment/",
                    "body_example": {
                        "restaurant_id": restaurant.restaurant_id,
                        "dish_ids": [dish1.dish_id, dish2.dish_id],
                        "payment_type": "upi"
                    }
                },
                "get_user_orders": {
                    "method": "GET",
                    "url": f"{base_url}/api/users/{user.user_id}/orders/"
                },
                "get_order_detail": "Once an order is placed, use the returned 'order_id' in this endpoint: "
                                    f"{base_url}/orders/{{order_id}}/",
                "send_order_for_delivery": "Use after order is 'preparing': "
                                           f"{base_url}/orders/{{order_id}}/send/",
                "mark_order_delivered": "Use after order is 'delivering': "
                                        f"{base_url}/orders/{{order_id}}/deliver/"
            }

        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
