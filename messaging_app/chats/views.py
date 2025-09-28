from django.shortcuts import render
from rest_framework import viewsets,status,filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from chats.filters import MessageFilter
from chats.pagination import DefaultPagination
from chats.permissions import IsParticipantOfConversation
from .models import Conversation, Message
from .serializers import ConversationSerializer,MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset=Conversation.objects.all()
    serializer_class=ConversationSerializer
    filter_backends=[filters.SearchFilter, filters.OrderingFilter]
    filter_class=MessageFilter
    search_fields=['participants__email']
    permission_classes=[IsAuthenticated,IsParticipantOfConversation]
    
    @action(detail=True,methods=['post'])
    def send_message(self,request,pk=None):
        conversation=get_object_or_404(Conversation,pk=pk)
        if request.user not in conversation.participants.all():
            return Response({"detail": "you are not a participant of this conversation"}, status=status.HTTP_403_FORBIDDEN,)
        serializer=MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user,conversation=conversation)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing messages.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["conversation", "sent_at", "sender"]

    def get_queryset(self):
        """Return messages in conversations where user is a participant with filtering."""

        # pylint: disable=no-member
        queryset = Message.objects.filter(
            conversation__participants__user=self.request.user
        ).select_related("sender", "conversation")

        # Additional filtering based on query parameters
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)

        sender_id = self.request.query_params.get("sender")
        if sender_id:
            queryset = queryset.filter(sender_id=sender_id)

        sent_after = self.request.query_params.get("sent_after")
        if sent_after:
            queryset = queryset.filter(sent_at__gte=sent_after)

        sent_before = self.request.query_params.get("sent_before")
        if sent_before:
            queryset = queryset.filter(sent_at__lte=sent_before)

        return queryset.order_by("-sent_at")

    def perform_create(self, serializer):
        """Set sender to current user and validate conversation participation."""
        conversation = serializer.validated_data["conversation"]

        # Verify user is a participant in the conversation
        if not conversation.participants.filter(user=self.request.user).exists():
            raise serializers.ValidationError(
                "You are not a participant in this conversation"
            )

        serializer.save(sender=self.request.user)