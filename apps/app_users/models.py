from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    """
    Default custom user model for apps.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    REQUIRED_FIELDS = []

    @property
    def name(self):
        return self.get_full_name()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.
        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.username})
