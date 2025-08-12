
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Candidates, Profile



# Asynchronous imports
from asgiref.sync import sync_to_async, async_to_sync
import asyncio

@sync_to_async
def render_template(request, template, context):
    return render(request, template, context)

@sync_to_async
def login_async(request, user):
    return login(request, user)

@sync_to_async
def logout_async(request):
    return logout(request)

@sync_to_async
def get_candidates(role=None):
    if role is None:
        return Candidates.objects.all().order_by('-votes')
    return Candidates.objects.filter(role=role).order_by('-votes')

@sync_to_async
def count_votes():
    return Profile.objects.filter(voted_ombudman=True, voted_comptroller=True).count()

@sync_to_async
def count_users():
    return User.objects.filter(is_superuser = False).count()
@sync_to_async
def get_user_by_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

@sync_to_async
def get_profiles():
    return Profile.objects.all()

@sync_to_async
def superuser_required(request):
    if request.user.is_superuser:
        return True
    return False

@sync_to_async
def sum_votes(candidates):
    return sum(candidate.votes for candidate in candidates)

@sync_to_async
def save_candidate(candidate):
    candidate.save()
    return candidate