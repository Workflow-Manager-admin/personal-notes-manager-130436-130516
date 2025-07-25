from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# PUBLIC_INTERFACE
class Note(models.Model):
    """
    Note model, each note is linked to a user (owner).
    """
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.owner.username})"
