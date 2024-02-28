
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# from team.models import Team

def signup(request):
    form = UserCreationForm()
    return render(request, 'userprofile/signup.html')