from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Utilisateur, Enseignant, Apprenant,
    EmailVerificationToken, PasswordResetToken
)
from .emails import (  # pyright: ignore[reportMissingImports]
    send_verification_email,
    send_password_reset_email,
    send_welcome_email
)


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data         = request.data
        email        = data.get('email')
        mot_de_passe = data.get('mot_de_passe')
        nom          = data.get('nom')
        prenom       = data.get('prenom')
        role         = data.get('role', 'apprenant')

        if not all([email, mot_de_passe, nom, prenom]):
            return Response(
                {'error': 'email, mot_de_passe, nom et prenom sont obligatoires'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Utilisateur.objects.filter(email=email).exists():
            return Response(
                {'error': 'Un compte existe déjà avec cet email'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = Utilisateur.objects.create_user(
            email=email,
            password=mot_de_passe,
            nom=nom,
            prenom=prenom,
        )
        user.is_active = False
        user.save()

        if role == 'enseignant':
            Enseignant.objects.create(
                utilisateur=user,
                specialite=data.get('specialite', '')
            )
        else:
            Apprenant.objects.create(
                utilisateur=user,
                niveau_etude=data.get('niveau_etude', '')
            )

        token_obj = EmailVerificationToken.objects.create(utilisateur=user)
        send_verification_email(user, token_obj.token)

        return Response(
            {'message': f'Compte créé. Un email de vérification a été envoyé à {email}. Vérifiez votre boîte mail.'},
            status=status.HTTP_201_CREATED
        )


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            token_obj = EmailVerificationToken.objects.get(
                token=token, is_used=False
            )
        except EmailVerificationToken.DoesNotExist:
            return Response(
                {'error': 'Lien invalide ou déjà utilisé'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = token_obj.utilisateur
        user.is_active   = True
        user.is_verified = True
        user.save()

        token_obj.is_used = True
        token_obj.save()

        send_welcome_email(user)

        return Response(
            {'message': f'Email confirmé ✅ Bienvenue {user.prenom} ! Vous pouvez maintenant vous connecter.'},
            status=status.HTTP_200_OK
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email        = request.data.get('email')
        mot_de_passe = request.data.get('mot_de_passe')

        user = authenticate(request, username=email, password=mot_de_passe)

        if not user:
            return Response(
                {'error': 'Email ou mot de passe incorrect'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'error': 'Veuillez confirmer votre email avant de vous connecter.'},
                status=status.HTTP_403_FORBIDDEN
            )

       # update last_login
        from django.utils import timezone
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        tokens = get_tokens(user)

        return Response({
            'message': 'Connexion réussie ✅',
            'user': {
                'id':          user.pk,
                'email':       user.email,
                'nom':         user.nom,
                'prenom':      user.prenom,
                'is_verified': user.is_verified,
            },
            'tokens': tokens
        })


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({
            'id':               u.pk,
            'nom':              u.nom,
            'prenom':           u.prenom,
            'email':            u.email,
            'is_verified':      u.is_verified,
            'date_inscription': str(u.date_inscription),
        })


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        try:
            user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            return Response(
                {'message': 'Si cet email existe, un lien de réinitialisation a été envoyé.'}
            )

        PasswordResetToken.objects.filter(utilisateur=user).delete()
        token_obj = PasswordResetToken.objects.create(utilisateur=user)
        send_password_reset_email(user, token_obj.token)

        return Response(
            {'message': 'Un lien de réinitialisation a été envoyé à votre email.'}
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        nouveau_mot_de_passe = request.data.get('nouveau_mot_de_passe')

        if not nouveau_mot_de_passe:
            return Response(
                {'error': 'nouveau_mot_de_passe est obligatoire'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token_obj = PasswordResetToken.objects.get(
                token=token, is_used=False
            )
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'error': 'Lien invalide ou déjà utilisé'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = token_obj.utilisateur
        user.set_password(nouveau_mot_de_passe)
        user.save()

        token_obj.is_used = True
        token_obj.save()

        return Response(
            {'message': 'Mot de passe réinitialisé ✅ Vous pouvez maintenant vous connecter.'}
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Déconnexion réussie ✅'})
        except Exception:
            return Response(
                {'error': 'Token invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )