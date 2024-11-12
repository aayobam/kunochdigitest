from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from apps.orders.custom_filter import OrderFilter
from .serializers import CreateOrderSerializer, GetOrdersAndTotalRevenueSerializer
from .models import Order
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


class OrderViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = Order.objects.select_related("customer").all()
    serializer_class = GetOrdersAndTotalRevenueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = OrderFilter

    def get_serializer_class(self):
        if self.action == "create_order":
            return CreateOrderSerializer
        return super().get_serializer_class()

    def paginate_results(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic
    @action(["POST"], detail=False, url_path="create-order")
    def create_order(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=["GET"], detail=False, url_path="get-orders-and-revenue")
    def get_orders_and_revenue(self, request):
        data = self.paginate_results(self.queryset)
        return Response(data, status=status.HTTP_200_OK)