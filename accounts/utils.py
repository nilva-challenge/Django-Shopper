from django.contrib.auth import get_user_model



User = get_user_model()

def get_user(email):
    user = User.objects.filter(email=email)
    if user.exists():
        return User.objects.first()
    else:
        return None
