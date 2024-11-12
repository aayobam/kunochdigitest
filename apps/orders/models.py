from django.db import models
from django.urls import reverse
from apps.common.model import BaseModel
from apps.users.models import CustomUser


class Order(BaseModel):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ("-date_created",)
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.id} for {self.customer.email}"

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"order_id": self.id})
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)