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

    def validate_email(self, value):
        email = value.strip().lower()
        existing = Doctor.objects.filter(email__iexact=email)
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise serializers.ValidationError(
                "A doctor with this email is already registered."
            )
        return email

    def validate_contact_number(self, value):
        cleaned_phone = "".join(filter(str.isdigit, value))
        if len(cleaned_phone) != 10:
            raise serializers.ValidationError("Contact number must contain 10 digits.")

        existing = Doctor.objects.filter(contact_number=cleaned_phone)
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise serializers.ValidationError(
                "A doctor with this contact number is already registered."
            )

        return cleaned_phone

    def validate_experience_years(self, value):
        if value < 0 or value > 70:
            raise serializers.ValidationError(
                "Experience years must be between 0 and 70."
            )
        return value

    def validate_name(self, value):
        cleaned_name = value.strip()
        if len(cleaned_name) < 2:
            raise serializers.ValidationError(
                "Doctor name must be at least 2 characters long."
            )
        return cleaned_name
