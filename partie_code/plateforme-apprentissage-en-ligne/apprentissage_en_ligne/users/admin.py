from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Utilisateur, Enseignant, Apprenant,
    Administrateur, EmailVerificationToken,
    PasswordResetToken
)


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    ordering     = ('email',)
    list_display = ('email', 'nom', 'prenom', 'is_verified', 'is_active', 'is_staff')
    list_filter  = ('is_verified', 'is_active', 'is_staff')
    search_fields = ('email', 'nom', 'prenom')
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'date_naissance')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'email', 'nom', 'prenom',
                'password1', 'password2'
            )
        }),
    )


@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display  = ('utilisateur', 'specialite')
    search_fields = ('utilisateur__email', 'specialite')


@admin.register(Apprenant)
class ApprenantAdmin(admin.ModelAdmin):
    list_display  = ('utilisateur', 'niveau_etude')
    search_fields = ('utilisateur__email',)


@admin.register(Administrateur)
class AdministrateurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'niveau_acces')


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display  = ('utilisateur', 'token', 'is_used', 'created_at')
    list_filter   = ('is_used',)
    search_fields = ('utilisateur__email',)


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display  = ('utilisateur', 'token', 'is_used', 'created_at')
    list_filter   = ('is_used',)
    search_fields = ('utilisateur__email',)