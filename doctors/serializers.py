from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialization",
            "contact_number",
            "email",
            "experience_years",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_contact_number(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError(
                "Contact number must contain at least 10 digits."
            )
        return value

    def validate_experience_years(self, value):
        if value < 0 or value > 80:
            raise serializers.ValidationError(
                "Experience years must be between 0 and 80."
            )
        return value
