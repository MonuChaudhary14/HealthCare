from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.email")

    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "age",
            "gender",
            "contact_number",
            "address",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def validate_name(self, value):
        cleaned_name = value.strip()
        if len(cleaned_name) < 2:
            raise serializers.ValidationError(
                "Patient name must be at least 2 characters long."
            )
        return cleaned_name

    def validate_age(self, value):
        if value <= 0 or value > 120:
            raise serializers.ValidationError("Age must be between 1 and 120.")
        return value

    def validate_contact_number(self, value):
        cleaned_phone = "".join(filter(str.isdigit, value))
        if len(cleaned_phone) != 10:
            raise serializers.ValidationError("Contact number must contain 10 digits.")
        return cleaned_phone

    def validate_address(self, value):
        cleaned_address = value.strip()
        if len(cleaned_address) < 3:
            raise serializers.ValidationError(
                "Address must be at least 3 characters long."
            )
        return cleaned_address

    def validate(self, attrs):
        request = self.context.get("request")

        name = attrs.get("name") or (self.instance.name if self.instance else "")
        contact_number = attrs.get("contact_number") or (
            self.instance.contact_number if self.instance else ""
        )

        if request and request.user.is_authenticated and name and contact_number:
            existing_query = Patient.objects.filter(
                created_by=request.user,
                name__iexact=name.strip(),
                contact_number=contact_number.strip(),
            )

            if self.instance:
                existing_query = existing_query.exclude(pk=self.instance.pk)

            if existing_query.exists():
                raise serializers.ValidationError(
                    {
                        "non_field_errors": [
                            "You have already added a patient with this name and contact number."
                        ]
                    }
                )

        return attrs
