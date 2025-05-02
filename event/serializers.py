from rest_framework import serializers

from .models import Event, Question, Answer, InviteLink, Location, GuestEvent


class EventSerializer(serializers.ModelSerializer) :
    location = serializers.SlugRelatedField(
        slug_field='location',
        queryset=Location.objects.all(),
        required=False,
        allow_null=True  # optional but good to add
    )
    guest = serializers.SerializerMethodField()

    class Meta :
        model = Event
        fields = ['id', 'title', 'description', 'approval', 'capacity', 'location', 'start', 'end', 'organizer', 'image_url', 'guest']
        read_only_fields = ['id', 'organizer']

    def get_guest(self, obj) :
        return obj.guest_events.count()


class QuestionSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Question
        fields = ['text', 'question_type', 'required']

        
class AnswerSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Answer
        fields = ['question', 'guest', 'answer_text', 'answer_choice']


class InviteLinkSerializer(serializers.ModelSerializer) :
    link = serializers.SerializerMethodField()

    class Meta :
        model = InviteLink
        fields = ['link']

    def get_link(self, obj) :
        return obj.get_shortened_link()
    

class LocationSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Location
        fields = '__all__'


class RegisterEventSerializer(serializers.ModelSerializer) :
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta :
        model = GuestEvent
        fields = ['user_name', 'event', 'ticket', 'approval_status', 'status']