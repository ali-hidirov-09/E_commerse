from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from .services.flash_sale import FlashSaleListCreateView

router = DefaultRouter()
router.register(r"products",ProductViewSet )
router.register(r"reviews", ReviewViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"customer", CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('sale/',FlashSaleListCreateView.as_view(), name='sale' ),
    # path('check_sale/<int:product_id>/', )
]

