from rest_framework import serializers
from .models import User,Message,Conversation,UserManager

class UserSerializer(serializers.ModelSerializer):
    user_id=serializers.UUIDField(read_only=True)
    password=serializers.CharField(write_only=True)
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    email=serializers.EmailField()
    role=serializers.CharField()
    

    class Meta:
        model=User
        fields=(
            "user_id",
            "password",
            "first_name",
            "last_name",
            "email",
            "role",
            "created_at",
        )
    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            password=validated_data['password']
        )

class MessageSerializer(serializers.ModelSerializer):
    message_id=serializers.UUIDField(read_only=True)
    sender=UserSerializer(read_only=True)
    message_body=serializers.CharField()
    
    conversation=serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all(), required=False, allow_null=True)
    
    sent_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model=Message
        fields=("message_id", "sender","conversation", "message_body", "sent_at")

    def validate(self, attrs):
        if "message_body" in attrs and not attrs["message_body"].strip():
            raise serializers.ValidationError({"message_body": "Message body cannot be blank"})
        request=self.context.get("request")
        conversation= attrs.get("conversation")
        if request and request.user.is_authenticated and conversation:
            if not conversation.participants.filter(pk=request.user.pk).exists():
                raise serializers.ValidationError("sender must be a participant of the conversation")
        return attrs

class ConversationSerializer(serializers.ModelSerializer):
    conversation_id=serializers.UUIDField(read_only=True)
    participants=serializers.SerializerMethodField()
    participants_id=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True, source="participants")

    messages= serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields=("conversation_id", "participants", "participants_id", "created_at", "messages")

    def get_participants(self,obj):
        return UserSerializer(obj.participants.all(), many=True).data
    
    def get_messages(self,obj):
        qs=obj.messages.order_by("sent_at").all()
        return MessageSerializer(qs, many=True, context=self.context).data
    
    def validate(self,attrs):
        participants=attrs.get("participants",[])
        request=self.context.get('request')

        if request and request.user.is_authenticated:
            total_participants=len(participants)+1
        else:
            total_participants=len(participants)
        if total_participants < 2:
            raise serializers.ValidationError({"participants": "A conversation must have at least two participants"})
        return attrs
    def create(self, validated_data):
        participants=validated_data.pop("participants",[])
        conv=Conversation.objects.create(**validated_data)
        request=self.context.get('request')
        if request and request.user.is_authenticated:
            participants.append(request.user)
        if participants:
            conv.participants.set(participants)
        return conv
    def update(self,instance,validated_data):
        participants=validated_data.pop("participants",None)
        instance=super().update(instance,validated_data)
        if participants is not None:
            instance.participants.set(participants)
        return instance
