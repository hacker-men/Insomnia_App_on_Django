from django.db import models
from users.models import Profile

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Sender")
    content = models.TextField("Message")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.sender}: {self.content[:30]}"