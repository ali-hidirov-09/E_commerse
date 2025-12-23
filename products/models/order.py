from django.contrib.auth.models import User
from django.db import models
from .product import Product
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+77\d{9}$',
    message="Phone number must be in the format: +77XXXXXXXXX"
)


class Order(models.Model):
    PENDING = 'Pending'         # ZAKAZ KETTI BAZAGA
    PROGRESSING = 'Progressing' # ADMINLAR ZAKAZNI KO'RIB UPAKOVKALANDI
    SHIPPED = 'Shipped'         # YUKLANDI
    DELIVERED = 'Delivered'     # YETKAIZB BERILDI
    CANCELED = 'Canceled'       # OTKAZ QILINDI

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROGRESSING, 'Progressing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True, null=True)

    def set_status(self, new_status):
        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError("Invalid Status")
        self.status = new_status
        self.save()

    def is_transition_allowed(self, new_status):
        allowed_transitions = {
            self.PENDING: [self.PROGRESSING, self.CANCELED],
            self.PROGRESSING: [self.SHIPPED, self.CANCELED],
            self.SHIPPED: [self.DELIVERED, self.CANCELED]
        }
        return new_status in allowed_transitions.get(self.status, [])

    def __str__(self):
        return f"Order{self.product.name} by {self.customer.username}"


