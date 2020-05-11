from django.db import models
from django.contrib.auth.models import AbstractUser
from encrypted_model_fields.fields import EncryptedTextField

class AzureADUser(AbstractUser):
    display_name = models.CharField(max_length=255, null=True)
    user_principal_name = models.CharField(max_length=255, null=False)
    class Meta:
        db_table = 'azure_ad_users'

class TokenCache(models.Model):
    user_object_id = models.CharField(null=True, max_length=255)
    refresh_token = EncryptedTextField(null=True)
    access_tokens = EncryptedTextField(null=True)
    class Meta:
        db_table = 'token_cache'