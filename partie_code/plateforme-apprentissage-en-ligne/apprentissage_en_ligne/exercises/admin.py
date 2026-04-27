from django.contrib import admin
from .models import Exercice, Soumission


@admin.register(Exercice)
class ExerciceAdmin(admin.ModelAdmin):
    list_display  = ('pk', 'cours', 'type', 'difficulte', 'score_minimum')
    list_filter   = ('type', 'difficulte')
    search_fields = ('enonce', 'cours__titre')


@admin.register(Soumission)
class SoumissionAdmin(admin.ModelAdmin):
    list_display  = ('apprenant', 'exercice', 'score', 'is_correct', 'date')
    list_filter   = ('is_correct',)
    search_fields = ('apprenant__utilisateur__email',)