from django.db.models import *
from abstract.base_model import BaseModel
from apps.user.models import User
from apps.restaurant.models import MenuItem, Restaurant
from external.enum import OrderStatus, PaymentStatus


# Create your models here.
class Orders(BaseModel):
    user = ForeignKey(User, on_delete=CASCADE)
    restaurant = ForeignKey(Restaurant, on_delete=CASCADE)
    item = ForeignKey(MenuItem, on_delete=CASCADE)
    quantity = IntegerField(default=0)
    total_price = FloatField(default=0.0)
    order_status = CharField(max_length=20, choices=OrderStatus.choices(), default=OrderStatus.PENDING.value)
    payment_status = CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING.value)
    transaction_id = CharField(max_length=100, blank=True, null=True)
    traking_id = CharField(max_length=5,  unique=True, editable=False)

    def __str__(self) -> str:
        return f"{self.user.first_name} + {self.user.last_name}"
    class Meta:
        db_table = 'order'
        ordering = ['created_at']
