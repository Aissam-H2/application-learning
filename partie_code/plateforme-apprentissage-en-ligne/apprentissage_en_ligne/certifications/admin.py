from django.contrib import admin
from .models import Inscription, Certification


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display  = ('apprenant', 'cours', 'progression', 'is_completed', 'date_inscription')
    list_filter   = ('is_completed',)
    search_fields = ('apprenant__utilisateur__email', 'cours__titre')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display    = ('inscription', 'code_validation', 'date_emission')
    search_fields   = ('code_validation', 'inscription__apprenant__utilisateur__email')
    readonly_fields = ('code_validation',)