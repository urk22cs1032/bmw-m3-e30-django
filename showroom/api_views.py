from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from .models import Vehicle
from .serializers import VehicleSerializer, VehicleWriteSerializer


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().order_by("-created_at", "-pk")
    permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return VehicleWriteSerializer
        return VehicleSerializer
