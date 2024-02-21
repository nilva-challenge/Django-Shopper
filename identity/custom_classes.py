from django.core.cache import cache
from rest_framework_simplejwt.tokens import AccessToken


class CacheManager:
    """
    Manager class for handling caching of access tokens.

    Methods:
    - set_cache_token(user: User, timeout_minutes: int = 60) -> AccessToken:
        Set the access token in the cache for the given user.

        Args:
        - user (User): The user for whom the access token is generated.
        - timeout_minutes (int): The timeout duration for the cache in minutes.

        Returns:
        - AccessToken: The access token.

    - get_cache_token(user_id: int) -> AccessToken or None:
        Retrieve the access token from the cache for the given user ID.

        Args:
        - user_id (int): The ID of the user for whom to retrieve the access token.

        Returns:
        - AccessToken or None: The access token if found, otherwise None.

    - delete_cache_token(user: User) -> bool or None:
        Delete the access token from the cache for the given user.

        Args:
        - user (User): The user for whom to delete the access token.

        Returns:
        - bool or None: True if the token is deleted successfully, otherwise None.
    """
    @staticmethod
    def set_cache_token(user, timeout_minutes: int = 60) -> AccessToken:
        """
        Set the access token in the cache for the given user.

        Args:
        - user (User): The user for whom the access token is generated.
        - timeout_minutes (int): The timeout duration for the cache in minutes.

        Returns:
        - AccessToken: The access token.
        """
        try:
            token = AccessToken.for_user(user)
            cache_key = f"token_{user.id}"
            cache.set(cache_key, token, timeout=timeout_minutes * 60)
            return token
        except Exception as e:
            print(f"Error setting cache token: {e}")

    @staticmethod
    def get_cache_token(user_id: int) -> AccessToken | None:
        """
        Retrieve the access token from the cache for the given user ID.

        Args:
        - user_id (int): The ID of the user for whom to retrieve the access token.

        Returns:
        - AccessToken or None: The access token if found, otherwise None.
        """
        try:
            cache_key = f"token_{user_id}"
            stored_token = cache.get(cache_key)
            return stored_token
        except Exception as e:
            print(f"Error getting cache token: {e}")
            return None

    @staticmethod
    def delete_cache_token(user) -> bool | None:
        """
        Delete the access token from the cache for the given user.

        Args:
        - user (User): The user for whom to delete the access token.

        Returns:
        - bool or None: True if the token is deleted successfully, otherwise None.
        """
        try:
            cache_key = f"token_{user.id}"
            cache.delete(cache_key)
            return True
        except Exception as e:
            print(f"Error deleting cache token: {e}")
            return None
