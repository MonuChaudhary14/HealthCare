from rest_framework import serializers

from doctors.models import Doctor
from doctors.serializers import DoctorSerializer
from patients.models import Patient
from patients.serializers import PatientSerializer

from .models import PatientDoctorMapping


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        source="patient",
        write_only=True,
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        source="doctor",
        write_only=True,
    )
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            "id",
            "patient_id",
            "doctor_id",
            "patient",
            "doctor",
            "assigned_at",
        ]
        read_only_fields = ["id", "patient", "doctor", "assigned_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        patient = attrs.get("patient")
        doctor = attrs.get("doctor")

        if request and request.user.is_authenticated:
            if patient.created_by != request.user:
                raise serializers.ValidationError(
                    {
                        "patient_id": [
                            "You do not have permission to assign doctors to this patient."
                        ]
                    }
                )

        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        "This doctor is already assigned to the selected patient."
                    ]
                }
            )

        return attrs
