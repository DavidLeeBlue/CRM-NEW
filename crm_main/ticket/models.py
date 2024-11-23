from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    CHOICES_PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )

    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    CLOSED = 'closed'

    CHOICES_STATUS = (
        (OPEN, 'Open'),
        (IN_PROGRESS, 'In Progress'),
        (CLOSED, 'Closed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=CHOICES_PRIORITY, default=MEDIUM)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=OPEN)
    created_by = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='ticket_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username
