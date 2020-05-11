
import datetime
import json

from .models import TokenCache

def get(user_object_id, resource):
    token_cache = TokenCache.objects.filter(user_object_id=user_object_id).first()
    if not token_cache:
        return None
    
    access_tokens = json.loads(token_cache.access_tokens)
    access_token = next((access_token for access_token in access_tokens if access_token['resource'] == resource), None)
    
    if access_token:
        return {
            'access_token': access_token['value'],
            'expires_on': datetime.datetime.fromtimestamp(access_token['expires_on']),
            'refresh_token': token_cache.refresh_token
        } 
    else:
        return {
            'access_token': None,
            'refresh_token': token_cache.refresh_token
        } 


def update(user_object_id, resource, token):
    token_cache, created = TokenCache.objects.get_or_create(user_object_id=user_object_id)
  
    access_tokens = json.loads(token_cache.access_tokens) if token_cache.access_tokens else []
    access_token = next((access_token for access_token in access_tokens if access_token['resource'] == resource), None)
    
    if not access_token:
        access_token = { 'resource': resource }
        access_tokens.append(access_token)

    expires_on = datetime.datetime.utcnow() + datetime.timedelta(seconds=token.get('expires_in'))
    access_token['value'] = token['access_token']
    access_token['expires_on'] = expires_on.timestamp()

    token_cache.refresh_token = token['refresh_token']
    token_cache.access_tokens = json.dumps(access_tokens)
    token_cache.save()

def delete(user_object_id):
    TokenCache.objects.filter(user_object_id=user_object_id).delete()