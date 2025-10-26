from django.shortcuts import render
from rest_framework import viewsets,status,filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import MessagePagination, ConversationPagination
from .permissions import (
    IsParticipantOfConversation,
    IsMessageSenderOrParticipant,
)


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
    search_fields=['participants__first_name','participants__email']
    permission_classes=[IsParticipantOfConversation,IsAuthenticated]
    
    @action(detail=True,methods=['post'])
    def send_message(self,request,pk=None):
        conversation=get_object_or_404(Conversation,pk=pk)
        if request.user not in conversation.participants.all():
            return Response({"detail": "you are not a participant of this conversation"}, status=status.HTTP_403_FORBIDDEN,)
        serializer=MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user,conversation=conversation)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        queryset = Conversation.objects.filter(participants=self.request.user).distinct()

        first_name = self.request.query_params.get('participants__first_name')
        if first_name:
            queryset = queryset.filter(participants__first_name__iexact=first_name).distinct()

        return queryset
from rest_framework_simplejwt.authentication import JWTAuthentication

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages within a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]  # Only this permission class
    authentication_classes = [JWTAuthentication]  # This ensures 401 for missing/invalid token
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sender__email']  # Enable filtering by sender email
    search_fields = ['message_body', 'sender__email', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['sent_at', 'sender__email']
    ordering = ['sent_at']
    pagination_class = DefaultPagination  # Use DefaultPagination (10 items/page)

    def get_queryset(self):
        """
        Filter messages by a `conversation_id` from the URL.
        Ensures user is a participant of the conversation.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        if conversation_pk:
            return Message.objects.filter(
                conversation__conversation_id=conversation_pk,
                conversation__participants=self.request.user
            ).select_related('sender', 'conversation')
        return Message.objects.none()

    def check_conversation_exists(self):
        """Check if conversation exists and return it or raise NotFound."""
        conversation_pk = self.kwargs.get('conversation_pk')
        try:
            return Conversation.objects.get(conversation_id=conversation_pk)
        except Conversation.DoesNotExist:
            raise NotFound("Conversation does not exist.")

    def check_permissions(self, request):
        """Check permissions after verifying conversation exists."""
        super().check_permissions(request)
        conversation = self.check_conversation_exists()
        if request.user not in conversation.participants.all():
            self.permission_denied(
                request,
                message="You are not a participant of this conversation."
            )

    def perform_create(self, serializer):
        """Set the sender and conversation after all permission checks."""
        conversation = self.check_conversation_exists()
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation.")
        serializer.save(sender=self.request.user, conversation=conversation)