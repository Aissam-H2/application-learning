from django.core.mail import send_mail
from django.conf import settings


def send_verification_email(utilisateur, token):
    verification_link = f"{settings.FRONTEND_URL}/api/users/verify-email/{token}/"

    subject = "Confirmez votre email — Plateforme Apprentissage"

    message = f"""
Bonjour {utilisateur.prenom} {utilisateur.nom},

Merci de vous être inscrit sur notre plateforme d'apprentissage en ligne.

Cliquez sur le lien ci-dessous pour activer votre compte :

👉 {verification_link}

Ce lien est valable 24 heures.

Si vous n'avez pas créé de compte, ignorez cet email.

Cordialement,
L'équipe Plateforme Apprentissage
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[utilisateur.email],
        fail_silently=False,
    )


def send_password_reset_email(utilisateur, token):
    reset_link = f"{settings.FRONTEND_URL}/api/users/reset-password/{token}/"

    subject = "🔐 Réinitialisation de votre mot de passe"

    message = f"""
Bonjour {utilisateur.prenom} {utilisateur.nom},

Vous avez demandé la réinitialisation de votre mot de passe.

Cliquez sur le lien ci-dessous :

👉 {reset_link}

Ce lien expire dans 1 heure.

Si vous n'avez pas fait cette demande, ignorez cet email.

Cordialement,
L'équipe Plateforme Apprentissage
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[utilisateur.email],
        fail_silently=False,
    )


def send_welcome_email(utilisateur):
    subject = "✅ Bienvenue sur la Plateforme Apprentissage !"

    message = f"""
Bonjour {utilisateur.prenom} {utilisateur.nom},

Votre compte a été activé avec succès. Bienvenue !

Vous pouvez maintenant vous connecter et commencer à apprendre.

Cordialement,
L'équipe Plateforme Apprentissage
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[utilisateur.email],
        fail_silently=False,
    )