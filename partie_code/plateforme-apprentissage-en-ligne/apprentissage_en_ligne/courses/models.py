from django.db import models
from users.models import Enseignant # pyright: ignore[reportMissingImports]


class Module(models.Model):
    titre        = models.CharField(max_length=255)
    type_contenu = models.CharField(max_length=100)
    contenu      = models.TextField()
    order        = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.titre


class Cours(models.Model):
    module            = models.ForeignKey(
        Module, on_delete=models.CASCADE,
        related_name='cours'
    )
    enseignant        = models.ForeignKey(
        Enseignant, on_delete=models.CASCADE,
        related_name='cours_crees'
    )
    titre             = models.CharField(max_length=255)
    description       = models.TextField()
    niveau_difficulte = models.IntegerField(default=1)
    duree             = models.FloatField(help_text='heures')

    class Meta:
        verbose_name_plural = 'Cours'

    def __str__(self):
        return self.titre