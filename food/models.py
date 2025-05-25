from django.db import models

class Restaurant(models.Model):
    restaurant_id = models.CharField(primary_key=True, max_length=36, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class Dish(models.Model):
    dish_id = models.CharField(primary_key=True, max_length=36, editable=False)
    restaurant_id = models.ForeignKey(Restaurant, related_name='dishes', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.restaurant_id.name})"

class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=36, editable=False)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name



class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('preparing', 'Preparing'),
        ('delivering', 'Delivering'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_TYPE_CHOICES = [
        ('upi', 'UPI'),
        ('cod', 'Cash On Delivery'),
        ('credit', 'Credit Card'),
    ]
    order_id = models.CharField(primary_key=True, max_length=36, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    status = models.CharField(
        max_length=15,
        choices=ORDER_STATUS_CHOICES,
        default='preparing'
    )

    # Used ManyToManyField in Order to automatically create a join table between the dishes and orders 
    items = models.ManyToManyField(Dish)

    def __str__(self):
        return f"Order #{self.order_id} by {self.user.name} from {self.restaurant_id.name}"