from django.db import models
from django.contrib.auth.models import User
from pages.models import Currency

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=False, null=False)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    encrypted_password = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Профіль користувача'
        verbose_name_plural = 'Профілі користувачів'

    

