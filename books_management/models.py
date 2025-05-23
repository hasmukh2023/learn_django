from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Book(models.Model):
    READING_STATUS = (
        ('not_started', 'Not Started'),
        ('reading', 'Currently Reading'),
        ('completed', 'Completed')
    )

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    reading_status = models.CharField(max_length=20, choices=READING_STATUS, default='not_started')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
