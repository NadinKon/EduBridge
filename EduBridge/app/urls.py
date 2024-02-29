from django.urls import path
from .views import ProductListView, LessonListView, ProductStatsView, GrantAccessView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path(
        "products/<int:product_id>/lessons/",
        LessonListView.as_view(),
        name="lesson-list",
    ),
    path("product-stats/", ProductStatsView.as_view(), name="product-stats"),
    path(
        "products/<int:product_id>/grant-access/",
        GrantAccessView.as_view(),
        name="grant-access",
    ),
]
