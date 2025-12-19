from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('dashboard-redirect/', views.dashboard_redirect, name='dashboard_redirect'),
    
    # Client URLs
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('client/create-request/', views.create_request, name='create_request'),
    
    # Organizer URLs
    path('organizer/dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
    path('organizer/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('organizer/reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('organizer/create-event/', views.create_event, name='create_event_standalone'), # Manual creation
    path('organizer/create-event/<int:request_id>/', views.create_event, name='create_event'), # From Request
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('organizer/request/<int:request_id>/', views.request_detail, name='request_detail'),
    
    # Participant URLs
    path('participant/dashboard/', views.participant_dashboard, name='participant_dashboard'),
    path('participant/join/<int:event_id>/', views.join_event, name='join_event'),
    
    # Sponsor URLs
    path('sponsor/dashboard/', views.sponsor_dashboard, name='sponsor_dashboard'),
    path('sponsor/fund/<int:event_id>/', views.sponsor_event, name='sponsor_event'),
]