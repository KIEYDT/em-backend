import os

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import EventViewSet, AddQuestionViewSet, SubmitAnswerViewSet, QuestionViewSet, AnswerViewSet, InviteLinkViewSet, GetInviteLinkViewSet, LocationViewSet, PastEventView, RandomEventImageView, RegisterEventView, OverviewViewSet, CheckRegistrationView


router = DefaultRouter()
router.register(r'event', EventViewSet, basename='view-event')
router.register(r'past', PastEventView, basename='view-past-event')
router.register(r'question', QuestionViewSet, basename='view-question')
router.register(r'question/add', AddQuestionViewSet, basename='add-question')
router.register(r'answer', AnswerViewSet, basename='view-answer')
router.register(r'answer/submit', SubmitAnswerViewSet, basename='submit-answer')
# router.register(r'invite', InviteLinkViewSet, basename='view-invite-link')
# router.register(r'invite/create', CreateInviteLinkViewSet, basename='create-invite-link')
router.register(r'location', LocationViewSet, basename='location')
# router.register(r'random-image-url', RandomEventImageView, basename='random-image-url')

overview_list = OverviewViewSet.as_view({
    'get': 'list',
    'patch': 'partial_update',
})

urlpatterns = [
    path('', include(router.urls)),
    path('random-image-url/', RandomEventImageView.as_view(), name='random-image-url'),
    path('invite/<str:hashed_id>', InviteLinkViewSet.as_view(), name='invite-link'),
    path('invite/gen/<int:event_id>', GetInviteLinkViewSet.as_view(), name='get-or-create-invite-link'),
    path('register/check/<str:invite_code>/', RegisterEventView.as_view(), name='check-registration'),
    path('register/event/<str:invite_code>/', RegisterEventView.as_view(), name='register-event'),
    path('overview/ticket/<int:ticket_id>', overview_list, name='overview-list'),
    path('overview/<int:event_id>/', overview_list, name='overview'),
    path('<str:hashed_id>/', InviteLinkViewSet.as_view(), name='invite-direct'),
]

