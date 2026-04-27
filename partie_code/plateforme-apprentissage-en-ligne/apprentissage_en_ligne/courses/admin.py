from django.contrib import admin
from .models import Cours, Module


class CoursInline(admin.TabularInline):
    model  = Cours
    extra  = 1
    fields = ('titre', 'enseignant', 'niveau_difficulte', 'duree')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display  = ('titre', 'type_contenu', 'order')
    list_filter   = ('type_contenu',)
    search_fields = ('titre',)
    inlines       = [CoursInline]


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display  = ('titre', 'module', 'enseignant', 'niveau_difficulte', 'duree')
    list_filter   = ('niveau_difficulte', 'module')
    search_fields = ('titre', 'description')