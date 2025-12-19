from django.shortcuts import render, redirect, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login
from django.utils import timezone
from .models import ClientRequest, Event, Registration, Sponsorship
from .forms import ClientRequestForm, EventForm, ReviewForm, SponsorshipForm,CustomUserCreationForm
from .decorators import organizer_required, client_required, participant_required, sponsor_required

# --- HOMEPAGE ---
def home(request):
    return render(request, 'core/home.html')

# --- CLIENT VIEWS ---
@user_passes_test(client_required)
def client_dashboard(request):
    requests = ClientRequest.objects.filter(client=request.user)
    return render(request, 'core/client_dashboard.html', {'requests': requests})

@user_passes_test(client_required)
def create_request(request):
    if request.method == 'POST':
        form = ClientRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.client = request.user
            req.save()
            messages.success(request, 'Request submitted successfully!')
            return redirect('client_dashboard')
    else:
        form = ClientRequestForm()
    return render(request, 'core/create_request.html', {'form': form})

# --- ORGANIZER VIEWS ---
@user_passes_test(organizer_required)
def organizer_dashboard(request):
    # Organizers see ALL pending requests and THEIR events
    pending_requests = ClientRequest.objects.filter(status='PENDING')
    my_events = Event.objects.filter(organizer=request.user)
    return render(request, 'core/organizer_dashboard.html', {
        'pending_requests': pending_requests,
        'my_events': my_events
    })

@user_passes_test(organizer_required)
def accept_request(request, request_id):
    req = get_object_or_404(ClientRequest, id=request_id)
    if request.method == 'POST':
        req.status = 'ACCEPTED'
        req.is_approved = True
        req.save()
        # Redirect to create event with this request linked
        return redirect('create_event', request_id=req.id)
    return render(request, 'core/accept_request_confirm.html', {'req': req})

@user_passes_test(organizer_required)
def create_event(request, request_id=None):
    client_req = None
    if request_id:
        client_req = get_object_or_404(ClientRequest, id=request_id)

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            
            if client_req:
                event.client_request = client_req
                # --- NEW CODE START ---
                # Automatically copy the budget from the request to the event
                if not event.budget and client_req.budget:
                    event.budget = client_req.budget
                # --- NEW CODE END ---
                
            event.save()
            messages.success(request, 'Event Created!')
            return redirect('organizer_dashboard')
    else:
        # Pre-fill data if coming from a client request
        initial_data = {}
        if client_req:
            initial_data = {
                # We can also pre-fill the form field if you want the organizer to see/edit it first
                'budget': client_req.budget, 
                'description': f"Requirements: {client_req.requirements}"
            }
        form = EventForm(initial=initial_data)
        
    return render(request, 'core/create_event.html', {'form': form})

@user_passes_test(organizer_required)
def request_detail(request, request_id):
    req = get_object_or_404(ClientRequest, id=request_id)
    return render(request, 'core/request_detail.html', {'req': req})

@login_required
def event_detail(request, event_id):
    # Fetch the event or show 404 if it doesn't exist
    event = get_object_or_404(Event, id=event_id)
    
    # (Optional) Security: Ensure only the organizer can manage their own event
    if request.user.role == 'ORGANIZER' and event.organizer != request.user:
        messages.error(request, "You are not authorized to manage this event.")
        return redirect('organizer_dashboard')

    return render(request, 'core/event_detail.html', {'event': event})


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Fetch all sponsorships for this event to list them
    sponsorships = event.sponsorships.all() 
    
    # Calculate total sponsorship amount (optional, but nice to have)
    total_sponsorship = sum(s.amount for s in sponsorships)

    return render(request, 'core/event_detail.html', {
        'event': event,
        'sponsorships': sponsorships,
        'total_sponsorship': total_sponsorship
    })

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'core/create_event.html', {'form': form, 'title': 'Edit Event'})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('organizer_dashboard')
    return redirect('event_detail', event_id=event.id)

# --- PARTICIPANT VIEWS ---
@user_passes_test(participant_required)
def participant_dashboard(request):
    # Show events that are active and registration is open
    upcoming_events = Event.objects.filter(is_active=True, registration_deadline__gte=timezone.now())
    my_registrations = Registration.objects.filter(participant=request.user)
    return render(request, 'core/participant_dashboard.html', {
        'events': upcoming_events,
        'registrations': my_registrations
    })

@user_passes_test(participant_required)
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Check if already registered
    if Registration.objects.filter(participant=request.user, event=event).exists():
        messages.warning(request, "You have already joined this event.")
    else:
        Registration.objects.create(participant=request.user, event=event)
        messages.success(request, "Successfully registered! Check your dashboard for the QR code.")
    return redirect('participant_dashboard')


@user_passes_test(participant_required)
def participant_dashboard(request):
    # Fetch active upcoming events
    upcoming_events = Event.objects.filter(is_active=True, registration_deadline__gte=timezone.now())
    
    # Fetch user's registrations
    my_registrations = Registration.objects.filter(participant=request.user)
    
    # NEW LOGIC: Get the list of Event objects the user has already joined
    # We use this in the template to show "Already Registered" instead of "Join"
    registered_event_ids = my_registrations.values_list('event_id', flat=True)
    user_registered_events = Event.objects.filter(id__in=registered_event_ids)

    return render(request, 'core/participant_dashboard.html', {
        'events': upcoming_events,
        'registrations': my_registrations,
        'user_registered_events': user_registered_events, # Pass this new variable
    })

# --- SPONSOR VIEWS ---
@user_passes_test(sponsor_required)
def sponsor_dashboard(request):
    active_events = Event.objects.filter(is_active=True)
    my_sponsorships = Sponsorship.objects.filter(sponsor=request.user)
    return render(request, 'core/sponsor_dashboard.html', {
        'events': active_events,
        'sponsorships': my_sponsorships
    })

@user_passes_test(sponsor_required)
def sponsor_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = SponsorshipForm(request.POST, request.FILES)
        if form.is_valid():
            sponsorship = form.save(commit=False)
            sponsorship.sponsor = request.user
            sponsorship.event = event
            sponsorship.save()
            messages.success(request, 'Sponsorship submitted!')
            return redirect('sponsor_dashboard')
    else:
        form = SponsorshipForm()
    return render(request, 'core/sponsor_event.html', {'form': form, 'event': event})

#organizer rejecting clients request
@user_passes_test(organizer_required)
def reject_request(request, request_id):
    req = get_object_or_404(ClientRequest, id=request_id)
    if request.method == 'POST':
        req.status = 'REJECTED'
        req.save()
        messages.info(request, 'Request has been rejected.')
    return redirect('organizer_dashboard')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard_redirect')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard_redirect(request):
    user = request.user
    
    if user.role == 'CLIENT':
        return redirect('client_dashboard')
    elif user.role == 'ORGANIZER':
        return redirect('organizer_dashboard')
    elif user.role == 'PARTICIPANT':
        return redirect('participant_dashboard')
    elif user.role == 'SPONSOR':
        return redirect('sponsor_dashboard')
    elif user.is_superuser:
        return redirect('/admin/')
        
    # Fallback if no role is assigned
    return redirect('home')