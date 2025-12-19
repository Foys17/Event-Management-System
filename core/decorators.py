from django.contrib.auth.decorators import user_passes_test

def organizer_required(user):
    return user.is_authenticated and user.role == 'ORGANIZER'

def client_required(user):
    return user.is_authenticated and user.role == 'CLIENT'

def participant_required(user):
    return user.is_authenticated and user.role == 'PARTICIPANT'

def sponsor_required(user):
    return user.is_authenticated and user.role == 'SPONSOR'