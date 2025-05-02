from hashids import Hashids
import os
import random as rand

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.conf import settings
from django.templatetags.static import static

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from .models import Event, Question, Answer, InviteLink, Location, GuestEvent
from .serializers import EventSerializer, QuestionSerializer, AnswerSerializer, InviteLinkSerializer, LocationSerializer, RegisterEventSerializer
from .permissions import IsOwnerOrReadOnly

from users.authentication import CookieJWTAuthenticatation
from users.models import Organizer
from ticket.models import Ticket

class EventViewSet(viewsets.ModelViewSet) :
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        
        if user.is_staff:
            queryset = self.queryset
        else:
            organizer = Organizer.objects.get(user=user)
            queryset = self.queryset.filter(organizer=organizer)
        try :
            queryset = queryset.filter(start__gte=now)
            if queryset.exists() :
                return queryset
        except :
            queryset = queryset.filter(start__lte=now, end__gte=now)
        return queryset
    
    def create(self, request) :
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid() :
            try : 
                organizer = Organizer.objects.get(user=request.user)
                organizer.events += 1
                organizer.save()
                serializer.save(organizer=organizer)
                return Response(serializer.data, status=HTTP_201_CREATED)
            except Organizer.DoesNotExist :
                return Response(
                    {"error": "The user does not exist."},
                    status=HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

class PastEventView(viewsets.ModelViewSet) :
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        now = timezone.now()

        if user.is_staff:
            queryset = self.queryset
        else:
            organizer = Organizer.objects.get(user=user)
            queryset = self.queryset.filter(organizer=organizer)

        queryset = queryset.filter(end__lt=now)
        return queryset
    

class AddQuestionViewSet(viewsets.ModelViewSet) :
    permission_classes = [IsAuthenticated]

    def create(self, request, event_id) :
        try :
            event = Event.objects.get(id=event_id, organizer__user=request.user)
            data = request.data
            for question_data in data :
                Question.objects.create(event=event, **question_data)
            return Response({ "message": "Question add success" }, status=201)
        except Event.DoesNotExist :
            return Response({ "error": "Event not found"}, status=404)
        

class SubmitAnswerViewSet(viewsets.ModelViewSet) :
    permission_classes = [AllowAny]

    def create(self, request, event_id) :
        try :
            event = Event.objects.get(id=event_id)
            answers = request.data
            for answer_data in answers :
                question_id = answer_data['question_id']
                question = Question.objects.get(id=question_id, event=event)
                Answer.objects.create(
                    event=event,
                    question=question,
                    guest=request.user,
                    answer_text=answer_data.get('answer_text', None),
                    answer_choice=answer_data.get('answer_choice', None),
                )
                return Response({ "message": "Ansers submitted"}, status=201)
        except Event.DoesNotExist :
            return Response({ "error": "Event is not found"}, status=404)
        except Question.DoesNotExist :
            return Response({ "error": "Question is not found"}, status=404)
        

class QuestionViewSet(viewsets.ModelViewSet) :
    permission_classes = [AllowAny]
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet) :
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerSerializer


class InviteLinkViewSet(APIView):
    permission_classes = [AllowAny]
    serializer_class = InviteLinkSerializer

    def get(self, request, hashed_id):
        try:
            hashids = Hashids(salt="invite_link_salt", min_length=8)
            decoded_id = hashids.decode(hashed_id)
            if not decoded_id:
                return Response({"error": "invalid invite link"}, status=400)

            invite_id = decoded_id[0]
            invite_link = get_object_or_404(InviteLink, id=invite_id)
            event = invite_link.event

            return Response({
                "title": event.title,
                "description": event.description,
                "location": event.location.location if event.location else None,
                "start": event.start.isoformat(),
                "end": event.end.isoformat(),
                "approvement required": event.approval,
                "capacity": "Unlimited" if event.capacity == -1 else event.capacity,
                "image_url": event.image_url if event.image_url else None,
                # Add other event fields as needed
            }, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
        

class GetInviteLinkViewSet(APIView) :
    permission_classes = [IsAuthenticated]
        
    def get(self, request, event_id) :
        try :
            event = get_object_or_404(Event, id=event_id, organizer__user=request.user)
            invite_link, _ = InviteLink.objects.get_or_create(event=event)
            return Response({
                "invite_link": invite_link.get_shortened_link(request)
            }, status=200)
        except Event.DoesNotExist:
            return Response({ "error": "Event not found" }, status=404)
        
        

class LocationViewSet(viewsets.ModelViewSet) :
    permission_classes = [AllowAny]
    serializer_class = LocationSerializer

    def create(self, request) :
        name = request.data.get('location')
        lat = request.data.get('lat')
        long = request.data.get('long')

        if not all([name, lat, long]) :
            # return Response({"error": "Missting require fields"}, status=HTTP_400_BAD_REQUEST)
            return Response({"message": "OK"}, status=HTTP_200_OK)
        
        location, created = Location.objects.get_or_create(
            location=name,
            defaults={
                'lat': lat,
                'long': long,
            },
        )

        serializer = self.get_serializer(location)

        if created :
            return Response(serializer.data, status=HTTP_201_CREATED)
        else :
            return Response(serializer.data, status=HTTP_200_OK)
        

class RandomEventImageView(APIView) :
    permission_classes = [AllowAny]

    def get(self, request) :
        image_dir = os.path.join(settings.MEDIA_ROOT, 'event', 'images')
        image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not image_files :
            return Response({"error": "No images found"}, status=HTTP_400_BAD_REQUEST)
        
        chosen_image = rand.choice(image_files)
        image_url = request.build_absolute_uri(f'{settings.MEDIA_URL}event/images/{chosen_image}')
        return Response({"image_url": image_url}, status=HTTP_200_OK)
    

class EventImageView(APIView) :
    permission_classes = [AllowAny]

    def get(self, request, event_id) :
        try :
            event = Event.objects.get(id=event_id)
            image_url = event.image.url if event.image else None
            if image_url :
                image_url = request.build_absoulute_uri(image_url)
            return Response({"image_url": image_url}, status=HTTP_200_OK)
        except Event.DoesNotExist :
            return Response({"error": "Event not found"}, status=HTTP_404_NOT_FOUND)
        except Exception as e :
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
        

class RegisterEventView(APIView) :
    permission_classes = [AllowAny]

    def get(self, request, invite_code) :
        hashids = Hashids(salt="invite_link_salt", min_length=8)
        decoded = hashids.decode(invite_code)

        if not decoded :
            return Response({ "error": "Invalid invite code" }, status=HTTP_400_BAD_REQUEST)
        
        invite_id = decoded[0]
        invite_link = get_object_or_404(InviteLink, id=invite_id)
        event = invite_link.event
        user = request.user
        try :
            if user.is_authenticated :
                guest_event = GuestEvent.objects.filter(user=user, event=event).first()
                if guest_event :
                    if event.approval :
                        return Response({"message": "You have successfully registered for the event, but it is pending approval",
                                         "approval_status": guest_event.approval_status,
                                         "registered": True}, status=HTTP_200_OK)
                    return Response({"registered": True}, status=HTTP_200_OK)
                else :
                    return Response({"registered": False}, status=HTTP_200_OK)
            else :
                return Response({"message": "User is not authenticated"}, status=HTTP_401_UNAUTHORIZED)
        except Exception as e :
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)

    def post(self, request, invite_code) :
        hashids = Hashids(salt="invite_link_salt", min_length=8)
        decoded = hashids.decode(invite_code)

        if not decoded :
            return Response({ "error": "Invalid invite code" }, status=HTTP_400_BAD_REQUEST)
        
        invite_id = decoded[0]
        invite_link = get_object_or_404(InviteLink, id=invite_id)
        event = invite_link.event

        if GuestEvent.objects.filter(event=event, user=request.user).exists() :
            return Response({ "error": "You are already registered for this event" }, status=HTTP_400_BAD_REQUEST)
        
        gen_ticket = Ticket.objects.create(user=request.user)
        GuestEvent.objects.create(event=event, user=request.user, ticket=gen_ticket)

        if event.approval :
            return Response({ "message": "You have successfully registered for the event, but it is pending approval",
                             "approval": True}, status=HTTP_201_CREATED)

        return Response({ "message": "You have successfully registered for the event" }, status=HTTP_201_CREATED)
    

class OverviewViewSet(viewsets.ModelViewSet) :
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterEventSerializer

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        return GuestEvent.objects.filter(event=event)
    
    def get_object(self):
        ticket_id = self.kwargs.get('ticket_id')
        return get_object_or_404(GuestEvent, ticket=ticket_id)
    
    def partial_update(self, request, *args, **kwargs):
        guest_event = self.get_object()
        response = request.data.get('approval_status', None)
        if guest_event.approval_status != GuestEvent.ApprovalStatus.PENDING and response :
            return Response({"error": "You have already approved or rejected this ticket"}, status=HTTP_400_BAD_REQUEST)
        try :
            if response == "approved" :
                guest_event.approval_status = GuestEvent.ApprovalStatus.APPROVED
            elif response == "rejected" :
                guest_event.approval_status = GuestEvent.ApprovalStatus.REJECTED
        except ValueError :
            return Response({"error": "Invalid approval status"}, status=HTTP_400_BAD_REQUEST)
        guest_event.save()
        return Response({"message": "Approval status updated"}, status=HTTP_200_OK)
    

class CheckRegistrationView(APIView) :
    permission_classes = [AllowAny]

    def get(self, request) :
        event_id = self.kwargs.get('event_id')
        user = request.user
        