from django.contrib import admin
from .models import Product, Access, Lesson, Group
from .services import add_user_to_group, redistribute_users


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "start_datetime", "cost")


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "access_granted_date")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Если создание (не изменение существующего), тогда добавляем пользователя в группу
        if not change:
            add_user_to_group(obj.user, obj.product)
            redistribute_users(obj.product)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "product")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "product", "min_users", "max_users")
