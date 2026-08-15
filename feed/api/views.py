from rest_framework import generics, permissions
from rest_framework.response import Response
from feed.api.serializers import FeedCalculationRequestSerializer, FeedCalculationSerializer
from feed.models import FeedCalculation
from feed.services import calculate_feed


class FeedCalculationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FeedCalculationSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return FeedCalculation.objects.none()
        return FeedCalculation.objects.filter(requested_by=self.request.user).select_related("rule")

    def create(self, request, *args, **kwargs):
        request_serializer = FeedCalculationRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        data = request_serializer.validated_data
        rule, result = calculate_feed(**data)
        record = FeedCalculation.objects.create(requested_by=request.user, rule=rule, inputs=data["inputs"], result=result, status=result["status"])
        return Response(FeedCalculationSerializer(record).data, status=201)
