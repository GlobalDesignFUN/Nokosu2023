from .models import User
from django.contrib.auth.forms import UserCreationForm

class PasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']