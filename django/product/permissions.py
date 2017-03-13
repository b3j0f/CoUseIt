"""Permisssion module."""
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser


class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    """Custom permission to only allow owners of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        """True iif method is safe or if owners are user."""
        result = super(IsOwnerOrReadOnly, self).has_object_permission(
            request, view, obj
        )

        if not result:
            result = obj.owners.filter(pk=request.user.id).exist()

        return result


class IsSupplierOrReadOnly(IsAuthenticatedOrReadOnly):
    """Custom permission to only allow suppliers of a supply to edit it."""

    def has_object_permission(self, request, view, obj):
        """True iif method is safe or if suppliers are user."""
        result = super(IsSupplierOrReadOnly, self).has_object_permission(
            request, view, obj
        )

        if not result:
            supplier = request.user.account

            for product in obj.products.all():
                if not product.suppliers.filter(pk=supplier.id).exist():
                    break

            else:
                result = True

        return result


class IsUserOrReadOnly(IsAuthenticatedOrReadOnly):
    """Custom permission to only allow users of an request to edit it."""

    def has_object_permission(self, request, view, obj):
        """True iif user method is safe or if user is a product user."""
        result = super(IsUserOrReadOnly, self).has_object_permission(
            request, view, obj
        )

        if not result:
            supplier = request.user.account

            for product in obj.products.all():
                if not product.users.filter(pk=supplier.id).exist():
                    break

            else:
                result = True

        return result
