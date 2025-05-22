# accounts/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from units.models import Unite

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Le nom d’utilisateur doit être renseigné")
        extra_fields.setdefault("role", User.ROLE_AGENT)
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        # Forcer le rôle admin et les flags staff/superuser
        extra_fields.setdefault("role", User.ROLE_ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("role") != User.ROLE_ADMIN:
            raise ValueError("Le superuser doit avoir le rôle 'admin'")
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Trois rôles :
    - admin     : gestion complète (superuser métier)
    - direction : lecture de toutes les unités
    - agent     : accès limité à une seule unité
    """
    ROLE_ADMIN     = 'admin'
    ROLE_DIRECTION = 'direction'
    ROLE_AGENT     = 'agent'

    ROLE_CHOICES = [
        (ROLE_ADMIN,     'Administrateur'),
        (ROLE_DIRECTION, 'Direction Centrale'),
        (ROLE_AGENT,     'Agent/Unité'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_AGENT,
        help_text="Rôle de l'utilisateur dans l'application"
    )
    unite = models.ForeignKey(
        Unite,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        help_text="Uniquement pour les agents : unité à laquelle ils appartiennent"
    )

    objects = UserManager()

    def save(self, *args, **kwargs):
        # Les admins et la direction n'ont pas d'unité
        if self.role in {self.ROLE_ADMIN, self.ROLE_DIRECTION}:
            self.unite = None
        # Les agents doivent obligatoirement avoir une unité
        elif self.role == self.ROLE_AGENT and self.unite is None:
            raise ValueError("Un agent doit obligatoirement appartenir à une unité.")
        super().save(*args, **kwargs)



