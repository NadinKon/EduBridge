from time import timezone
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product, Lesson, Access
from .serializers import ProductSerializer, LessonSerializer, ProductStatsSerializer
from .services import add_user_to_group, redistribute_users


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonListView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs.get("product_id")

        # Проверяем, имеет ли пользователь доступ к продукту
        if not Access.objects.filter(user=user, product_id=product_id).exists():
            raise PermissionDenied("У вас нет доступа к этому продукту.")

        # Возвращаем уроки, принадлежащие продукту
        return Lesson.objects.filter(product_id=product_id)


class ProductStatsView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductStatsSerializer


class GrantAccessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        user = request.user
        product = get_object_or_404(Product, pk=product_id)

        # Проверяем, не начался ли уже продукт
        if product.start_datetime <= timezone.now():
            return Response(
                {"error": "Продукт уже начался."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Добавляем пользователя в группу
        add_user_to_group(user, product)

        # Перераспределение пользователей
        redistribute_users(product)

        return Response(
            {"message": "Доступ к продукту предоставлен."}, status=status.HTTP_200_OK
        )
