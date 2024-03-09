from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms

# Create your models here.
class User(AbstractUser):
    pass

class Place(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    is_to_visit = models.BooleanField(default=False)
    category = models.CharField(max_length=50)

    STATE_CHOICES = (
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
    )
    state = models.CharField(max_length=500, choices=STATE_CHOICES)

    CATEGORY_CHOICES = (
    ('monument', 'Monument / Historical Site'),
    ('forest', 'Forest'),
    ('mountain', 'Hill Station'),
    ('beach', 'Beach'),
    ('lake', 'Lake'),
    ('park', 'Park'),
    ('trek', 'Trekking Destination'),
    ('mall', 'Shopping Mall'),
    )
    category = models.CharField(max_length=500, choices=CATEGORY_CHOICES)   


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'location', 'description', 'category', 'state']
        
