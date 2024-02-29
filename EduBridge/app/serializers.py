from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Lesson, Access


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "start_datetime", "cost", "lessons_count"]

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(product=obj).count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "video_url", "product"]


class ProductStatsSerializer(serializers.ModelSerializer):
    students_count = serializers.SerializerMethodField()
    groups_fill_percentage = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "students_count",
            "groups_fill_percentage",
            "purchase_percentage",
        ]

    def get_students_count(self, obj):
        # Количество учеников
        return Access.objects.filter(product=obj).count()

    def get_groups_fill_percentage(self, obj):
        # На сколько % заполнены группы
        groups = obj.groups.all()
        total_max = sum(group.max_users for group in groups)
        total_current = sum(group.users.count() for group in groups)
        return (total_current / total_max * 100) if total_max else 0

    def get_purchase_percentage(self, obj):
        # Процент приобретения продукта
        total_users = User.objects.count()
        access_count = Access.objects.filter(product=obj).count()
        return (access_count / total_users * 100) if total_users else 0
