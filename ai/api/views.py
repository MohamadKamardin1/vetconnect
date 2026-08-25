from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.api.serializers import AIDiseaseAssistRequestSerializer, AIFeedAssistRequestSerializer, AIInteractionSerializer
from ai.models import AIInteraction
from ai.services import invoke_ai_feature
from disease.services import assess_disease
from feed.services import calculate_feed


class AIDiseaseAssistView(APIView):
    """
    Wraps the existing deterministic disease decision-support engine (disease.services.assess_disease)
    with an optional, redacted AI narrative layer. The deterministic engine and its rule data are never
    modified by this endpoint. AI involvement never changes the possible_conditions, urgency, or
    referral_required computed locally; it can only append a non-authoritative narrative field.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=AIDiseaseAssistRequestSerializer, responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        request_serializer = AIDiseaseAssistRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        species_code = request_serializer.validated_data["species_code"]
        inputs = request_serializer.validated_data["inputs"]
        _rule, output = assess_disease(species_code=species_code, inputs=inputs)
        urgent = output.get("status") == "COMPLETED" and output.get("urgency") == "EMERGENCY"
        full_inputs = {**inputs, "species_code": species_code}
        result = invoke_ai_feature(user=request.user, feature_key="DISEASE_ASSIST", full_inputs=full_inputs, deterministic_fn=lambda: output, urgent=urgent)
        return Response(result, status=200)


class AIFeedAssistView(APIView):
    """
    Wraps the existing deterministic feed engine (feed.services.calculate_feed) with an optional,
    redacted AI narrative layer. The computed daily_feed_kg and assumptions are always the locally
    computed deterministic values; AI involvement can only append a non-authoritative narrative field.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=AIFeedAssistRequestSerializer, responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        request_serializer = AIFeedAssistRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        data = request_serializer.validated_data
        _rule, result = calculate_feed(species_code=data["species_code"], production_category=data["production_category"], inputs=data["inputs"])
        full_inputs = {**data["inputs"], "species_code": data["species_code"], "production_category": data["production_category"]}
        response = invoke_ai_feature(user=request.user, feature_key="FEED_ASSIST", full_inputs=full_inputs, deterministic_fn=lambda: result, urgent=False)
        return Response(response, status=200)


class AIInteractionListView(generics.ListAPIView):
    """Authenticated, user-scoped audit trail of AI interactions. No interaction from another user is ever returned."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AIInteractionSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return AIInteraction.objects.none()
        return AIInteraction.objects.filter(user=self.request.user)
