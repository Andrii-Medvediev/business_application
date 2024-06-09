from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Profile
from .encryption_util import load_key, decrypt_data

class EncryptedPasswordBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            key = load_key('users/encryption_key.key')
            decrypted_password = decrypt_data(profile.encrypted_password, key)

            if password == decrypted_password:
                return user
        except User.DoesNotExist:
            return None
        except Profile.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
