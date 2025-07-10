import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import JSONField  
from django.conf import settings
# If using PostgreSQL
# For Django 3.1+ JSONField is built-in in django.db.models.JSONField

class Order(models.Model):
    order_number = models.CharField(max_length=32, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.JSONField()  # or Postgres JSONField if needed
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Delivery information fields
    full_name = models.CharField(max_length=100, default='Unknown')
    street_address1 = models.CharField(max_length=80, default='Unknown')
    street_address2 = models.CharField(max_length=80, blank=True)
    town_or_city = models.CharField(max_length=40, default='Unknown')
    county = models.CharField(max_length=80, blank=True)
    postcode = models.CharField(max_length=20, default='Unknown')
    country = models.CharField(max_length=40, default='Unknown')

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def __str__(self):
        return self.order_number