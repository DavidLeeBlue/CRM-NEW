from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    APARTMENT = 'apartment'
    HOUSE = 'house'
    OFFICE = 'office'

    CHOICES_TYPE = (
        (APARTMENT, 'Apartment'),
        (HOUSE, 'House'),
        (OFFICE, 'Office'),
    )

    AVAILABLE = 'available'
    RENTED = 'rented'
    UNDER_MAINTENANCE = 'under_maintenance'

    CHOICES_STATUS = (
        (AVAILABLE, 'Available'),
        (RENTED, 'Rented'),
        (UNDER_MAINTENANCE, 'Under Maintenance'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=CHOICES_TYPE, default=APARTMENT)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=AVAILABLE)
    rooms = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(User, related_name='properties', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class PropertyComment(models.Model):
    property = models.ForeignKey(Property, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='property_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username

class PropertyCommentImage(models.Model):
    comment = models.ForeignKey(PropertyComment, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_comment_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)