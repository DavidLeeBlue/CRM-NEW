from django.db import models
from django.contrib.auth.models import User
from property.models import Property  # Import the Property model
from django.utils import timezone  # Import timezone

class Tenant(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='tenants', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    property = models.ForeignKey(Property, related_name='tenants', on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)  # Set default value
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class TenantImage(models.Model):
    tenant = models.ForeignKey(Tenant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tenant_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    tenant = models.ForeignKey(Tenant, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='tenant_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username

class CommentImage(models.Model):
    comment = models.ForeignKey(Comment, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='comment_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)