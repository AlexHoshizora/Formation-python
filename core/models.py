from django.db import models

# Create your models here.

class Enrollment(models.Model):
    first_name = models.CharField("Prénom", max_length=100)
    last_name = models.CharField("Nom", max_length=100)
    email = models.EmailField("Adresse e-mail")
    password = models.CharField("Mot de passe", max_length=128)
    amount = models.DecimalField("Montant payé", max_digits=8, decimal_places=2, default=199)
    created_at = models.DateTimeField("Date d'inscription", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} – {self.email}"


class Progress(models.Model):
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="progress",
    )
    last_module = models.PositiveIntegerField("Dernier module validé", default=0)
    last_section = models.CharField("Dernière partie", max_length=200, blank=True)
    updated_at = models.DateTimeField("Dernière mise à jour", auto_now=True)

    def __str__(self) -> str:
        return f"Progression de {self.enrollment}"
