from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from .services.flash_sale import FlashSaleListCreateView, check_flash_sale, FlashSaleListView
from .services.product_view_history import ProductViewHistoryCreate
from .services import admin_replenish_stock
from . import signals

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"reviews", ReviewViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"orders", OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('sale/', FlashSaleListCreateView.as_view(), name='sale'),
    path('sales/', FlashSaleListView.as_view(), name='sales_all'),
    path('check_sale/<int:product_id>/', check_flash_sale, name="check_sale"),
    path('product_view/', ProductViewHistoryCreate.as_view(), name="product-view-history-create"),
    path('stock/replenish_stock/<int:product_id>/<int:amount>/', admin_replenish_stock, name='stock_replenish_stock'),
]
