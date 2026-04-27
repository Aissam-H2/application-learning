import uuid
from django.db import models
from users.models import Apprenant
from courses.models import Cours


class Inscription(models.Model):
    apprenant        = models.ForeignKey(
        Apprenant, on_delete=models.CASCADE,
        related_name='inscriptions'
    )
    cours            = models.ForeignKey(
        Cours, on_delete=models.CASCADE,
        related_name='inscriptions'
    )
    date_inscription = models.DateField(auto_now_add=True)
    progression      = models.FloatField(default=0.0)
    is_completed     = models.BooleanField(default=False)

    class Meta:
        unique_together = ('apprenant', 'cours')
        verbose_name    = 'Inscription'

    def __str__(self):
        return f"{self.apprenant} → {self.cours}"


class Certification(models.Model):
    inscription     = models.OneToOneField(
        Inscription, on_delete=models.CASCADE,
        related_name='certification'
    )
    date_emission   = models.DateField(auto_now_add=True)
    code_validation = models.CharField(
        max_length=64, unique=True, editable=False
    )

    class Meta:
        verbose_name = 'Certification'

    def save(self, *args, **kwargs):
        if not self.code_validation:
            self.code_validation = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cert {self.code_validation[:8]}… — {self.inscription}"

    def verifier_authenticite(self, code: str) -> bool:
        return self.code_validation == code