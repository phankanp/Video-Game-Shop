from django.contrib.auth import get_user_model  # imports CustomUser model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# Extend base user forms and swap in CustomUser model.
# Displays email, username, and password fields
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)
