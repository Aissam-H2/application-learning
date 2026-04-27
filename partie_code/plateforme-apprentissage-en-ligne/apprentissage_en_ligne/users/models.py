import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, mot_de_passe=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password or mot_de_passe)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('nom', 'Admin')
        extra_fields.setdefault('prenom', 'Super')
        return self.create_user(email, password=password, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    nom              = models.CharField(max_length=100)
    prenom           = models.CharField(max_length=100)
    date_naissance   = models.DateField(null=True, blank=True)
    email            = models.EmailField(unique=True)
    date_inscription = models.DateField(auto_now_add=True)
    is_active        = models.BooleanField(default=False)  # False until email verified
    is_staff         = models.BooleanField(default=False)
    is_verified      = models.BooleanField(default=False)  # email verified flag

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']
    objects = UtilisateurManager()

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Enseignant(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE,
        related_name='enseignant', primary_key=True
    )
    specialite  = models.CharField(max_length=200)
    biographie  = models.TextField(blank=True)

    def __str__(self):
        return str(self.utilisateur)


class Apprenant(models.Model):
    utilisateur  = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE,
        related_name='apprenant', primary_key=True
    )
    niveau_etude = models.CharField(max_length=100)
    objectif     = models.TextField(blank=True)

    def __str__(self):
        return str(self.utilisateur)


class Administrateur(models.Model):
    utilisateur  = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE,
        related_name='administrateur', primary_key=True
    )
    niveau_acces = models.CharField(max_length=50, default='full')

    def __str__(self):
        return str(self.utilisateur)


class EmailVerificationToken(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE,
        related_name='verification_token'
    )
    token      = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used    = models.BooleanField(default=False)

    def __str__(self):
        return f"Token — {self.utilisateur.email}"


class PasswordResetToken(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE,
        related_name='password_reset_token'
    )
    token      = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used    = models.BooleanField(default=False)

    def __str__(self):
        return f"Reset Token — {self.utilisateur.email}"