import datetime

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from account import auth, token_cache, settings

from .graph_service import GraphService
from .models import AzureADUser
from .exceptions import AuthError



def sign_in(request):
    context = { 
        'title': 'Sign In'
    }
    return render(request,'account/sign_in.html', context)

def sign_in_azure_ad(request):
    authorize_url = auth.get_authorize_url(request)
    return redirect(authorize_url)

@csrf_exempt
def sign_in_azure_ad_callback(request): 
    error = request.POST.get('error')
    error_description = request.POST.get('error_description')
    if error:
        raise AuthError(error_description)

    authorization_code = request.POST.get('code')
    auth_result = auth.get_token_with_code(request, authorization_code, settings.GRAPH_RESOURCE)
    
    graph_service = GraphService(auth_result['access_token'])
    me = graph_service.get_me()

    user = _get_or_create_and_update_user(me)
    login(request, user)

    token_cache.update(request.user.username, settings.GRAPH_RESOURCE, auth_result)
    
    return redirect('/')

def sign_out(request):
    auth.delete_token_cache(request)
    logout(request)
    end_session_url = auth.get_end_session_url(request)
    return redirect(end_session_url)

def error(request):
    context = { 
        'title': 'Sign In',
        'type': request.GET.get('type'),
        'message': request.GET.get('message')
    }
    return render(request,'account/error.html', context) 

def _get_or_create_and_update_user(me):
    id = me.get('id')
    user, _ = AzureADUser.objects.get_or_create(username=id)
    if me.get('mail'):
        user.email = me.get('mail')
    if me.get('givenName'):
        user.first_name  = me.get('givenName')
    if me.get('surname'):
        user.last_name = me.get('surname')
    user.display_name = me.get('displayName')
    user.user_principal_name = me.get('userPrincipalName')
    user.save()
    return user