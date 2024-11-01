from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

class UserProfile(models.Model):

    GENDER_CHOICES = [
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other'),
    ]

    USER_TYPE_CHOICES = [
        ('fm', 'Farm Manager'),
        ('n', 'Nutritionist'),
        ('d', 'Distributor'),
        ('fso', 'Food Safety Officer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="UserProfile")
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    contact_no = models.CharField(max_length=20, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True)
    nid = models.CharField(max_length=18, null=True) 
    dob = models.DateField(null=True)
    address = models.TextField(null=True)
    profile_picture = models.ImageField(upload_to='profile_picture', null=True)
    user_type = models.CharField(max_length=3, choices=USER_TYPE_CHOICES, blank=False)
    user_identity = models.CharField(max_length=10, unique=True, editable=False, null=True)

    def __str__(self):
        return self.name

    def generate_user_id(self):
        prefix = dict(self.USER_TYPE_CHOICES).get(self.user_type, "")
        if(prefix == "Farm Manager"):
            prefix = "fm"

        elif(prefix == "Nutritionist"):
            prefix = "n"

        elif(prefix == "Distributor"):
            prefix = "d"

        elif(prefix == "Food Safety Officer"):
            prefix = "fso"
            
        count = UserProfile.objects.filter(user_type=self.user_type).count() + 1
        return f"{prefix}{count}"

    def save(self, *args, **kwargs):
        if not self.user_identity:
            self.user_identity = self.generate_user_id()
        super().save(*args, **kwargs)

@receiver(pre_delete, sender=UserProfile)
def delete_profile_pictures(sender, instance, **kwargs):
    if instance.profile_picture:
        if os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)
