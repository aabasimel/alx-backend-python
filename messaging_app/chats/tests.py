from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from .models import Conversation, Message, User

User = get_user_model()

# class ConversationViewSetTestCase(APITestCase):
#     """Test cases for ConversationViewSet"""

#     def setUp(self):
#         self.client = APIClient()

#         # Create test users with roles
#         self.usr1 = User.objects.create_user(
#             email='usr1@gmail.com',
#             password='test1',
#             first_name='usr1',
#             last_name='usr1',
#             role='guest'
#         )
#         self.usr2 = User.objects.create_user(
#             email='usr2@gmail.com',
#             password='test2',
#             first_name='usr2',
#             last_name='usr2',
#             role='guest'
#         )
#         self.usr3 = User.objects.create_user(
#             email='usr3@gmail.com',
#             password='test3',
#             first_name='usr3',
#             last_name='usr3',
#             role='host'
#         )
#         self.usr4 = User.objects.create_user(
#             email='usr4@gmail.com',
#             password='test4',
#             first_name='usr4',
#             last_name='usr4',
#             role='admin'
#         )
#         self.usr5 = User.objects.create_user(
#             email='usr5@gmail.com',
#             password='test5',
#             first_name='usr5',
#             last_name='usr5',
#             role='admin'
#         )
#         self.usr6 = User.objects.create_user(
#             email='usr6@gmail.com',
#             password='test6',
#             first_name='usr6',
#             last_name='usr6',
#             role='admin'
#         )

#         # Create a conversation with some participants
#         self.conversation = Conversation.objects.create()
#         self.conversation.participants.set([self.usr1, self.usr4])

    # def test_list_conversation_for_authenticated_user(self):
    #     self.client.force_authenticate(user=self.usr1)
    #     url = reverse('conversation-list')
    #     response = self.client.get(url)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data['results']), 1)
    # # def test_list_conversation_for_unauthenticated_user(self):
    # #     """Anonymous user should get 401 Unauthorized"""
    # #     self.client.force_authenticate(user=None)
    # #     url = reverse('conversation-list')
    # #     response = self.client.get(url)

    #     # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    # def test_list_conversation_for_non_participant_user(self):
    #     self.client.force_authenticate(user=self.usr2)  # usr2 is not in the conversation
    #     url = reverse('conversation-detail', args=[self.conversation.pk])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_create_conversations(self):
    #     self.client.force_authenticate(user=self.usr1)
    #     url = reverse('conversation-list')
    #     data = {
    #         'participants_id': [self.usr4.pk, self.usr3.pk]  # Use .id instead of email
    #     }
    #     response = self.client.post(url, data, format='json')

    #     print("Response data:", response.data)

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Conversation.objects.count(), 2)

    #     # Get the newly created conversation
    #     new_conversation = Conversation.objects.exclude(pk=self.conversation.pk).first()
    #     self.assertEqual(new_conversation.participants.count(), 3)
    #     self.assertIn(self.usr1, new_conversation.participants.all())
    #     self.assertIn(self.usr3, new_conversation.participants.all())
    #     self.assertIn(self.usr4, new_conversation.participants.all())

    # def test_create_conversatio_with_nonexistent_user(self):
    #     self.client.force_authenticate(user=self.usr1)
    #     url=reverse('conversation-list')
    #     data={
    #         'participants_id':[9999] # 9999 doestn't exist 
    #     }
    #     response=self.client.post(url,data,format='json')
    #     self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    # def test_retrieve_converstation_as_participants(self):
    #     self.client.force_authenticate(user=self.usr1)
    #     url=reverse('conversation-detail', args=[self.conversation.pk])
    #     response=self.client.get(url)
    #     print('responsedata',response.data)

    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertIn('conversation_id',response.data)
    #     self.assertIn('participants',response.data)

    
    # def test_update_converstation(self):
    #     self.client.force_authenticate(user=self.usr1)
    #     url=reverse('conversation-detail',args=[self.conversation.pk])
    #     data={
    #         'participants_id':[self.usr1.pk,self.usr2.pk,self.usr3.pk]
    #     }
    #     response=self.client.patch(url,data,format='json')

    #     print('updated response', response.data)
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.conversation.refresh_from_db()
    #     self.assertEqual(self.conversation.participants.count(),3)
    #     self.assertIn(self.usr2,self.conversation.participants.all())
    #     self.assertIn(self.usr2,self.conversation.participants.all())
    # def test_retrieve_converstatio_as_non_participant(self):
    #     self.client.force_authenticate(user=self.usr3)
    #     url=reverse('conversation-detail',args=[self.conversation.pk])
    #     response=self.client.get(url)
    #     print('response', response.data)

    #     self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    # def test_filter_converstaion_by_participants(self):
    #     """Test filting converstaion by paticipants name"""
    #     converstion2=Conversation.objects.create()
    #     converstion2.participants.set([self.usr1,self.usr2, self.usr6])
    #     self.client.force_authenticate(user=self.usr6)
    #     url=reverse('conversation-list')
    #     response = self.client.get(url, {'participants__first_name': 'usr6'})
        
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data['results']),1)
    
    # def test_filter_conversations_by_participant_email(self):
    #     """Test filtering conversations by participant email"""
    #     self.client.force_authenticate(user=self.usr1)
    #     url = reverse('conversation-list')
    #     response = self.client.get(url, {'participants__email': 'usr1@gmail.com'})

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data['results']), 1)

class MessagingSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.usr1 = User.objects.create_user(
            email='usr1@gmail.com',
            password='test1',
            first_name='usr1',
            last_name='usr1',
            role='guest'
        )
        self.usr2 = User.objects.create_user(
            email='usr2@gmail.com',
            password='test2',
            first_name='usr2',
            last_name='usr2',
            role='guest'
        )
        self.usr3 = User.objects.create_user(
            email='usr3@gmail.com',
            password='test3',
            first_name='usr3',
            last_name='usr3',
            role='host'
        )
        self.usr4 = User.objects.create_user(
            email='usr4@gmail.com',
            password='test4',
            first_name='usr4',
            last_name='usr4',
            role='admin'
        )
        self.usr5 = User.objects.create_user(
            email='usr5@gmail.com',
            password='test5',
            first_name='usr5',
            last_name='usr5',
            role='admin'
        )
        self.usr6 = User.objects.create_user(
            email='usr6@gmail.com',
            password='test6',
            first_name='usr6',
            last_name='usr6',
            role='admin'
        )

        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.usr1, self.usr4])

        self.message = Message.objects.create(
            conversation=self.conversation,
            sender=self.usr4,
            message_body="Hello usr1"
        )

#     def test_list_messages_as_participants(self):
#         self.client.force_authenticate(user=self.usr1)
#         url = reverse(
#         'messages-list',
#         kwargs={'conversation_pk': str(self.conversation.pk)}
# )
#         response = self.client.get(url)
#         print(response.data)

#         print("response", response.data)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 1)
    def test_create_message_as_participant(self):
        """Test creating a message as conversation participant"""
        self.client.force_authenticate(user=self.usr1)
        
        # Use the list URL for creating (POST), not detail URL
        # Also use self.conversation, not just 'conversation'
        url = reverse('conversation-message-list', kwargs={
            'conversation_pk': self.conversation.conversation_id
        })
        
        data = {
            'message_body': 'New test message'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 2)  # Should be 2, not 3 (1 from setUp + 1 new)
        self.assertEqual(response.data['sender']['email'], 'usr1@gmail.com')

    def test_create_message_as_non_participant_returns_403(self):
        """Non-participant should get 403 when posting to conversation messages."""
        # usr3 is not part of the conversation (participants: usr1, usr4)
        self.client.force_authenticate(user=self.usr3)
        url = reverse('conversation-message-list', kwargs={
            'conversation_pk': self.conversation.conversation_id
        })
        data = {
            'message_body': 'Attempt by non-participant'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Ensure no new message was created
        self.assertEqual(Message.objects.count(), 1)
