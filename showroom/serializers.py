from rest_framework import serializers

from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "id",
            "bmw_id",
            "model",
            "year",
            "variant",
            "price",
            "status",
            "image",
            "customer_name",
            "registration_number",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class VehicleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "bmw_id",
            "model",
            "year",
            "variant",
            "price",
            "status",
            "image",
            "customer_name",
            "registration_number",
        ]

    def validate_bmw_id(self, value):
        bmw_id = value.strip()
        if not bmw_id:
            raise serializers.ValidationError("BMW ID is required.")
        instance = getattr(self, "instance", None)
        if Vehicle.objects.filter(bmw_id__iexact=bmw_id).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("A vehicle with this BMW ID already exists.")
        return bmw_id

    def validate_registration_number(self, value):
        reg = value.strip() if value else ""
        instance = getattr(self, "instance", None)
        if reg:
            if Vehicle.objects.filter(registration_number__iexact=reg).exclude(pk=instance.pk if instance else None).exists():
                raise serializers.ValidationError("A vehicle with this registration number already exists.")
        return reg
