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

class Permissions(models.Model):
    name = models.CharField( 
        max_length=100
        )
    
    def __str__(self):
        return f'{self.name} Permission'
    
    class Meta:
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'


class PermissionsGroup(models.Model):
    permissions_id = models.ManyToManyField (
        Permissions, 
        related_name='permissions'
        )
    name = models.CharField (
        max_length=50,
    )
    
    class Meta:
        verbose_name = 'GroupPermission'
        verbose_name_plural = 'GroupPermissions'

    def __str__(self):
        return f'{self.name}'
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
    image = models.ImageField (
        default='default.jpg',
        upload_to='profile_images'
        )
     
    def __str__(self):
        return f'{self.user.username} Profile'
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def have_profile(self,user):
        try:
            profile = self.objects.get(user=user)
        except:
            return None
        return True, profile