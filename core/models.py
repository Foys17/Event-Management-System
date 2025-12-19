from django.contrib.auth.models import AbstractUser
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.utils import timezone  # Import timezone for defaults

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ORGANIZER', 'Organizer'),
        ('SPONSOR', 'Sponsor'),
        ('PARTICIPANT', 'Participant'),
        ('CLIENT', 'Client'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def is_organizer(self):
        return self.role == 'ORGANIZER'
    
    def is_sponsor(self):
        return self.role == 'SPONSOR'

    def is_participant(self):
        return self.role == 'PARTICIPANT'

    def is_client(self):
        return self.role == 'CLIENT'


# 1. Client Request Model
class ClientRequest(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    event_type = models.CharField(max_length=100)
    requirements = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='PENDING') # Pending, Accepted, Rejected


# 2. Event Model
class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    client_request = models.OneToOneField(ClientRequest, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    registration_deadline = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)

    def is_registration_open(self):
        return timezone.now() < self.registration_deadline


# 3. Registration (Participant) Model
class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations') 
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    
    registered_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def save(self, *args, **kwargs):
        # Auto-generate QR Code on save
        if not self.qr_code:
            qr_data = f"Event: {self.event.title}\nParticipant: {self.participant.username}\nID: {self.participant.id}"
            qr_img = qrcode.make(qr_data)
            canvas = BytesIO()
            qr_img.save(canvas, format='PNG')
            file_name = f'qr_{self.participant.username}_{self.event.id}.png'
            self.qr_code.save(file_name, File(canvas), save=False)
        super().save(*args, **kwargs)


# 4. Sponsorship Model
class Sponsorship(models.Model):
    # Fixed: Removed duplicate definitions. Used related_name='sponsorships'
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='sponsorships')
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsorships')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    branding_assets = models.FileField(upload_to='sponsors/', blank=True)
    
    # ADDED: Timestamp field needed for your template to show the date
    timestamp = models.DateTimeField(default=timezone.now) 


# 5. Review Model
class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()