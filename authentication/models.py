# authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    AUTHOR = 'Autheur'
    REVIEWER = 'Critique Littéraire'

    ROLE_CHOICES = (
        (AUTHOR, 'Auteur'),
        (REVIEWER, 'Critique Littéraire'),
    )
    profile_photo = models.ImageField(verbose_name='Photo de profil')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')