
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from rest_framework.authtoken.models import Token
from users.serializers import TokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request, *args, **kwargs):
    #return render(request, 'users/profile.html', {'token': Token.objects.get(user=request.user.id).key})
    return redirect('../api/profile/')
@login_required
@api_view(['GET'])
def profile_api(request, *args, **kwargs):
    serializer = TokenSerializer(Token.objects.get(user=request.user.id))
    return Response(serializer.data)