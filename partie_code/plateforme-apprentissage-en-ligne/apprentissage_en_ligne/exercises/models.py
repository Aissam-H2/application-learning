from django.db import models
from courses.models import Cours # pyright: ignore[reportMissingImports]


class Exercice(models.Model):
    TYPE_CHOICES = [
        ('qcm',  'QCM'),
        ('code', 'Code'),
        ('texte', 'Texte libre'),
    ]

    cours         = models.ForeignKey(
        Cours, on_delete=models.CASCADE,
        related_name='exercices',
           null=True, blank=True
    )
    type          = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default='qcm'
    )
    enonce        = models.TextField()
    reponse_correcte = models.TextField()
    difficulte    = models.IntegerField(default=1)
    score_minimum = models.FloatField(default=0.5)

    def __str__(self):
        return f'Exercice #{self.pk} — {self.cours.titre}'


class Soumission(models.Model):
    exercice   = models.ForeignKey(
        Exercice, on_delete=models.CASCADE,
        related_name='soumissions'
    )
    apprenant  = models.ForeignKey(
        'users.Apprenant', on_delete=models.CASCADE,
        related_name='soumissions'
    )
    reponse    = models.TextField()
    score      = models.FloatField(default=0.0)
    is_correct = models.BooleanField(default=False)
    date       = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('exercice', 'apprenant')

    def __str__(self):
        return f'{self.apprenant} — {self.exercice}'