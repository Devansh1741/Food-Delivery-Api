# 🍽️ Django Food Ordering System

A simple food ordering API system built with Django. It supports:

- Restaurant and Dish management
- User creation
- Placing and tracking orders
- Order status updates (preparing → delivering → delivered)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/food-ordering-django.git
cd food-ordering-django
```

```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

# Create and Activate Virtual Environment
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

# Install Dependencies
```
pip install -r requirements.txt
```

# Apply Migrations
```
python manage.py makemigrations
python manage.py migrate
```

# Create Superuser (for Admin Panel)
```
python manage.py createsuperuser
```

# Run the Development Server
```
python manage.py runserver
```

# 🧪 Sample Data and API Testing
✅ Create Sample Data
Use this endpoint to create a sample restaurant, user, and two dishes:
```
POST http://localhost:8000/setup/sample/
```
Response Example:
```
{
  "message": "Sample data created successfully",
  "data": {
    "restaurant": { ... },
    "user": { ... },
    "dishes": [ ... ]
  },
  "next_steps": {
    "make_order": {
      "method": "POST",
      "url": "http://localhost:8000/users/<user_id>/payment/",
      "body_example": {
        "restaurant_id": "<restaurant_id>",
        "dish_ids": ["<dish1_id>", "<dish2_id>"],
        "payment_type": "card"
      }
    },
    "get_user_orders": {
      "method": "GET",
      "url": "http://localhost:8000/users/<user_id>/orders/"
    },
    "get_order_detail": "http://localhost:8000/orders/{order_id}/",
    "send_order_for_delivery": "http://localhost:8000/orders/{order_id}/send/",
    "mark_order_delivered": "http://localhost:8000/orders/{order_id}/deliver/"
  }
}

```

You can now use Postman or cURL to:

- Place an Order via `POST /users/<user_id>/payment/`
- Check Orders via `GET /users/<user_id>/orders`
- Track a Specific Order via `GET /orders/{order_id}`
- Update Order Status to "Delivering" via `POST /orders/{order_id}/send`
- Mark as "Delivered" via `POST /orders/{order_id}/deliver/`



# 📁 Project Structure (Relevant Files)
```
food_ordering/
│
├── app/
│   ├── models.py         # Models: User, Restaurant, Dish, Order
│   ├── views.py          # Core logic and API endpoints
│   ├── urls.py           # URL routes
│
├── food_ordering/
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
└── requirements.txt
```
