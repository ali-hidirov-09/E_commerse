from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    agar egasi bo'lsa productsni ozgartira oladi , agar bo'lmasa faqatgina o'qiy oladi

    """

    def has_object_permission(self, request, view, obj):
        """Agar get zapros kelsa xammapdam ko'ra oladi aks holda egasi hisoblab True qaytaradi
        Maqsadi True yoki False qaytarish
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.customer == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    """ agar xodim staff member bo'lsa u edit va delete qila oladi """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
