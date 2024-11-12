from rest_framework import serializers
from apps.orders.models import Order
from django.db.models import Sum


class CreateOrderSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(required=True, max_length=100)
    price = serializers.DecimalField(max_digits = 10, decimal_places=2, default = 0.00)
    quantity = serializers.IntegerField(default = 0)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, default = 0.00)
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = '__all__'

    def creat(self, validated_data):
        validated_data["total_price"] = validated_data["price"] * validated_data["quantity"]
        validated_data["customer"] = self.context["request"].user
        return super().create(validated_data)
    
    def validate(self, attrs):
        if attrs["quantity"] <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        if attrs["price"] <= 0.00:
            raise serializers.ValidationError("Price must be greater than 0.00")
        return super().validate(attrs)


class GetOrdersAndTotalRevenueSerializer(serializers.Serializer):
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, default=0.00)
    
    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        total_revenue = self.Meta.model.objects.filter(date_created__range=['start_date', 'end_date']).aggregate(total_revenue=Sum('total_price'))['total_revenue']
        data['total_revenue'] = format(total_revenue, '.2f')
        return data