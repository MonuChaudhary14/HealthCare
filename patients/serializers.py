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

    def validate_age(self, value):
        if value <= 0 or value > 100:
            raise serializers.ValidationError("Age must be between 1 and 100.")
        return value

    def validate_contact_number(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError(
                "Contact number must contain at least 10 digits."
            )
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        name = attrs.get("name", self.instance.name if self.instance else "")
        contact_number = attrs.get(
            "contact_number",
            self.instance.contact_number if self.instance else "",
        )

        if request and request.user.is_authenticated:
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
