import hashlib
import hmac
import secrets
from django.conf import settings
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from messaging.api.serializers import ConversationCreateSerializer, ConversationSerializer, MessageSerializer, WebhookEndpointSerializer
from messaging.models import Conversation, ConversationParticipant, Message, WebhookEndpoint


class ConversationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return ConversationCreateSerializer if self.request.method == "POST" else ConversationSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Conversation.objects.none()
        return Conversation.objects.filter(participants__user=self.request.user).prefetch_related("participants__user", "messages__sender").distinct()

    @transaction.atomic
    def perform_create(self, serializer):
        conversation = Conversation.objects.create(created_by=self.request.user, subject=serializer.validated_data.get("subject", ""))
        ConversationParticipant.objects.bulk_create([ConversationParticipant(conversation=conversation, user_id=user_id) for user_id in serializer.validated_data["participant_ids"]])
        self._created_conversation = conversation

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(ConversationSerializer(self._created_conversation).data, status=status.HTTP_201_CREATED)


class ConversationDetailView(generics.RetrieveAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Conversation.objects.none()
        return Conversation.objects.filter(participants__user=self.request.user).prefetch_related("participants__user", "messages__sender")


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_conversation(self):
        return get_object_or_404(Conversation, pk=self.kwargs["conversation_id"], participants__user=self.request.user)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Message.objects.none()
        return Message.objects.filter(conversation__pk=self.kwargs["conversation_id"], conversation__participants__user=self.request.user).select_related("sender").distinct()

    def perform_create(self, serializer):
        conversation = self.get_conversation()
        try:
            with transaction.atomic():
                message, created = Message.objects.get_or_create(conversation=conversation, sender=self.request.user, client_message_id=serializer.validated_data["client_message_id"], defaults={"body": serializer.validated_data["body"]})
        except IntegrityError:
            message = Message.objects.get(conversation=conversation, sender=self.request.user, client_message_id=serializer.validated_data["client_message_id"])
            created = False
        self._message = message
        self._created = created

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(MessageSerializer(self._message).data, status=status.HTTP_201_CREATED if self._created else status.HTTP_200_OK)


class WebhookEndpointCreateView(generics.CreateAPIView):
    serializer_class = WebhookEndpointSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        secret = serializer.validated_data.pop("secret")
        secret_hash = hashlib.sha256(secret.encode()).hexdigest()
        self._endpoint = WebhookEndpoint.objects.create(owner=self.request.user, secret_hash=secret_hash, **serializer.validated_data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"id": str(self._endpoint.pk), "url": self._endpoint.url, "secret": "stored-as-hash"}, status=status.HTTP_201_CREATED)
