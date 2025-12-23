# from django.http import JsonResponse, HttpResponseBadRequest
# from  django.contrib.admin.views.decorators import staff_member_required
# from rest_framework.response import Response
# from products.models import Product
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAdminUser
#
# @api_view(['POST'])
# @swagger_auto_schema(operation_description="Admin replenishes stock for a product ")
# @permission_classes([IsAdminUser])
# def admin_replenish_stock(request, product_id, amount):
#     try:
#         product = Product.objects.get(id=product_id)
#         product.increase_stock(amount)
#         return Response({'status': 'success', 'message': f'Successfully replenished stock by {amount}'})
#     except ValueError:
#         return HttpResponseBadRequest('invalid input')

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from drf_yasg.utils import swagger_auto_schema


@api_view(['POST'])
@permission_classes([IsAdminUser])
@swagger_auto_schema(operation_description="Admin replenishes stock for a product")
def admin_replenish_stock(request, product_id, amount):
    try:
        product = Product.objects.get(id=product_id)
        product.increase_stock(amount)

        return Response(
            {
                "status": "success",
                "message": f"Successfully replenished stock by {amount}"
            },
            status=status.HTTP_200_OK
        )

    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except ValueError:
        return Response(
            {"error": "Invalid amount"},
            status=status.HTTP_400_BAD_REQUEST
        )
