from rest_framework import generics, permissions
from rest_framework.response import Response
from disease.api.serializers import DiseaseAssessmentRequestSerializer, DiseaseAssessmentSerializer
from disease.models import DiseaseAssessment
from disease.services import assess_disease


class DiseaseAssessmentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DiseaseAssessmentSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return DiseaseAssessment.objects.none()
        return DiseaseAssessment.objects.filter(requested_by=self.request.user).select_related("rule")

    def create(self, request, *args, **kwargs):
        request_serializer = DiseaseAssessmentRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        data = request_serializer.validated_data
        rule, output = assess_disease(**data)
        record = DiseaseAssessment.objects.create(requested_by=request.user, rule=rule, inputs=data["inputs"], output=output, status=output["status"])
        return Response(DiseaseAssessmentSerializer(record).data, status=201)
