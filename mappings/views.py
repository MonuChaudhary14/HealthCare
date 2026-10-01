from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer


class MappingListCreateView(generics.ListCreateAPIView):
    queryset = PatientDoctorMapping.objects.all().select_related("patient", "doctor")
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class MappingDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        mappings = PatientDoctorMapping.objects.filter(patient_id=pk).select_related(
            "patient", "doctor"
        )
        serializer = PatientDoctorMappingSerializer(
            mappings, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            mapping = PatientDoctorMapping.objects.get(pk=pk)
            if mapping.patient.created_by != request.user:
                return Response(
                    {"error": "You do not have permission to remove this mapping."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            mapping.delete()
            return Response(
                {"message": "Doctor assignment removed successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except PatientDoctorMapping.DoesNotExist:
            return Response(
                {"error": "Mapping record not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
