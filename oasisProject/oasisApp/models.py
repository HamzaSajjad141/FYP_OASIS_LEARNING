from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Import timezone

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=100, default='Pending')
    respond = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Complaint by {self.user.username}"

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField()
    query_text = models.TextField()
    translated_text = models.TextField()
    video_url = models.URLField()
    date = models.DateTimeField(default=timezone.now)  # Add this field

    def __str__(self):
        return f"History for {self.user.username}"
