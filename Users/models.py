from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BaseAuditModel(models.Model):
    created = models.DateTimeField(
        auto_now_add = True
    )
    last_updated = models.DateTimeField(
        auto_now = True
    )
    is_active = models.BooleanField(
        default=True
    )
    class Meta:
        abstract = True


class Profile(BaseAuditModel):
    user = models.OneToOneField (
        User, 
        on_delete=models.CASCADE
        )
    grade = models.CharField (
        max_length=50,
        default=''
        )
    identification = models.IntegerField (
        )
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Candidates(BaseAuditModel):
    profile = models.OneToOneField(
        Profile, 
        on_delete=models.CASCADE, 
        related_name='candidate_profile'
        )
    code = models.CharField(
        max_length=10,
        default=''
        )
    votes = models.IntegerField(
        default=0
        )
    description = models.TextField(
        max_length=500,
        default=''
        )
    image = models.ImageField(
        upload_to='candidates/',
        default='candidates/default_candidate.webp'
        )