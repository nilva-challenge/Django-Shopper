from django.core.cache import cache
from rest_framework_simplejwt.tokens import AccessToken



class CacheManager():
    @staticmethod
    def set_cache_token(user, timeout_minutes=60):
        try:
            token = AccessToken.for_user(user)
            cache_key = f"token_{user.id}"
            cache.set(cache_key, token, timeout=timeout_minutes * 60)
            return token  
        except Exception as e:
            print(f"Error setting cache token: {e}")

    @staticmethod
    def get_cache_token(user_id):
        try:
            cache_key = f"token_{user_id}"
            stored_token = cache.get(cache_key)
            return stored_token
        except Exception as e:
            print(f"Error getting cache token: {e}")
            return None

    @staticmethod
    def delete_cache_token(user):
        try:
            cache_key = f"token_{user.id}"
            cache.delete(cache_key)
            return True
        except Exception as e:
            print(f"Error deleting cache token: {e}")
            return None
