from django.db import models
from django.urls import reverse
from apps.common.model import BaseModel
from apps.users.models import CustomUser


class Employee(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    position = models.CharField(max_length=100)

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return self.position

    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={'id': self.id})