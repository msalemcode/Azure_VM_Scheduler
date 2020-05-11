import datetime
import uuid

from requests_oauthlib import OAuth2Session

from account import settings, token_cache
from .exceptions import AuthError, NoCachedTokenError

from website.settings import LOGIN_URL


def get_authorize_url(request):  
    nonce = uuid.uuid4().hex
    state = ''
    session = OAuth2Session(
        client_id=settings.CLIENT_ID,
        redirect_uri=_get_absolute_uri(request, settings.AUTH_CALLBACK_URL),
        scope='openid email offline_access ' + _get_site_scope_string_from_settings())
    auth_url, _ = session.authorization_url(
        settings.AUTHORIZE_ENDPOINT,
        state=state,
        response_mode='form_post',
        nonce=nonce)
    return auth_url

def get_token_with_code(request, authorization_code, resource):
    session = OAuth2Session(
        client_id=settings.CLIENT_ID,
        redirect_uri=_get_absolute_uri(request, settings.AUTH_CALLBACK_URL)
    )
    return session.fetch_token(
        settings.TOKEN_ENDPOINT,
        code=authorization_code,
        scope=_get_resource_scope_string_from_settings(resource),
        include_client_id=True,
        client_secret=settings.CLIENT_SECRET,
        
    )

def get_access_token(request, resource):
    token = token_cache.get(request.user.username, resource)
    if not token:
        raise NoCachedTokenError()   
    if not token['access_token'] or datetime.datetime.utcnow() > token['expires_on'] - datetime.timedelta(seconds=60*5):
        token = _refresh_token(request, token['refresh_token'], resource)
        token_cache.update(request.user.username, resource, token)
        print(token['access_token'])
    return token['access_token']

def refresh_token(request, resource):
    token = token_cache.get(request.user.username, resource)
    if not token:
        raise NoCachedTokenError()
    token = _refresh_token(request, token['refresh_token'], resource)
    print(token)
    token_cache.update(request.user.username, resource, token)

def delete_token_cache(request):
    token_cache.delete(request.user.username)

def get_end_session_url(request):
    post_logout_redirect_uri = _get_absolute_uri(request, LOGIN_URL[1:])
    return settings.END_SESSION_ENDPOINT + '?post_logout_redirect_uri=' + post_logout_redirect_uri

def _refresh_token(request, refresh_token, resource):
    session = OAuth2Session(
        client_id=settings.CLIENT_ID,
        redirect_uri=_get_absolute_uri(request, settings.AUTH_CALLBACK_URL), 
        scope=_get_resource_scope_string_from_settings(resource))
    return session.refresh_token(
        settings.TOKEN_ENDPOINT,
        refresh_token=refresh_token,
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET)

def _get_site_scope_string_from_settings():
    return ' '.join([_get_resource_scope_string(scope) for scope in settings.SCOPES])

def _get_resource_scope_string(scope):
    return ' '.join([scope['resource'] + permission for permission in scope['permissions']])

def _get_resource_scope_string_from_settings(resource):
    scope = next((scope for scope in settings.SCOPES if scope['resource'] == resource), None)
    if not scope:
        raise AuthError('No scope was found in account.settings for resource ' +resource)
    return _get_resource_scope_string(scope)

def _get_absolute_uri(request, relative_uri):
    scheme = request.scheme
    host = request.get_host()
    return '%s://%s/%s' % (scheme, host, relative_uri)