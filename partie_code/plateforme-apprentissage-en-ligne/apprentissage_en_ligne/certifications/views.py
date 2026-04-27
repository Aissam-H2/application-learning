from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import FileResponse

from .models import Inscription, Certification
from .serializers import (
    InscriptionSerializer,
    InscriptionCreateSerializer,
    CertificationSerializer
)
from .pdf import generate_certificate_pdf
from users.permissions import IsApprenant # pyright: ignore[reportMissingImports]


class EnrollView(APIView):
    permission_classes = [IsAuthenticated, IsApprenant]

    def post(self, request):
        serializer = InscriptionCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            inscription = serializer.save()
            return Response(
                InscriptionSerializer(inscription).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class MyInscriptionsView(APIView):
    permission_classes = [IsAuthenticated, IsApprenant]

    def get(self, request):
        inscriptions = Inscription.objects.filter(
            apprenant=request.user.apprenant
        )
        serializer = InscriptionSerializer(inscriptions, many=True)
        return Response(serializer.data)


class InscriptionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsApprenant]

    def get_object(self, pk, apprenant):
        try:
            return Inscription.objects.get(pk=pk, apprenant=apprenant)
        except Inscription.DoesNotExist:
            return None

    def get(self, request, pk):
        inscription = self.get_object(pk, request.user.apprenant)
        if not inscription:
            return Response(
                {'error': 'Inscription introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(InscriptionSerializer(inscription).data)

    def patch(self, request, pk):
        inscription = self.get_object(pk, request.user.apprenant)
        if not inscription:
            return Response(
                {'error': 'Inscription introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )

        progression = request.data.get('progression')
        if progression is None:
            return Response(
                {'error': 'progression est obligatoire'},
                status=status.HTTP_400_BAD_REQUEST
            )

        progression = float(progression)
        if not 0.0 <= progression <= 1.0:
            return Response(
                {'error': 'progression doit être entre 0.0 et 1.0'},
                status=status.HTTP_400_BAD_REQUEST
            )

        inscription.progression = progression

        if progression == 1.0 and not inscription.is_completed:
            inscription.is_completed = True
            inscription.save()

            cert = Certification.objects.create(inscription=inscription)

            return Response({
                'message':       'Cours complété ✅ Certificat généré !',
                'inscription':   InscriptionSerializer(inscription).data,
                'certification': CertificationSerializer(cert).data
            })

        inscription.save()
        return Response(InscriptionSerializer(inscription).data)

    def delete(self, request, pk):
        inscription = self.get_object(pk, request.user.apprenant)
        if not inscription:
            return Response(
                {'error': 'Inscription introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        inscription.delete()
        return Response(
            {'message': 'Désinscription réussie ✅'},
            status=status.HTTP_204_NO_CONTENT
        )


class MyCertificationsView(APIView):
    permission_classes = [IsAuthenticated, IsApprenant]

    def get(self, request):
        certifications = Certification.objects.filter(
            inscription__apprenant=request.user.apprenant
        )
        serializer = CertificationSerializer(certifications, many=True)
        return Response(serializer.data)


class DownloadCertificateView(APIView):
    """Download the certificate as a real PDF"""
    permission_classes = [IsAuthenticated, IsApprenant]

    def get(self, request, pk):
        try:
            cert = Certification.objects.get(
                pk=pk,
                inscription__apprenant=request.user.apprenant
            )
        except Certification.DoesNotExist:
            return Response(
                {'error': 'Certificat introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )

        buffer   = generate_certificate_pdf(cert)
        filename = f"certificat_{cert.code_validation[:8]}.pdf"

        return FileResponse(
            buffer,
            as_attachment=True,
            filename=filename,
            content_type='application/pdf'
        )


class VerifyCertificationView(APIView):
    """Anyone can verify a certificate by its code"""
    permission_classes = [AllowAny]

    def get(self, request, code):
        try:
            cert = Certification.objects.get(code_validation=code)
            return Response({
                'valid':            True,
                'apprenant':        str(cert.inscription.apprenant.utilisateur),
                'cours':            cert.inscription.cours.titre,
                'module':           cert.inscription.cours.module.titre,
                'date_emission':    str(cert.date_emission),
                'code_validation':  cert.code_validation
            })
        except Certification.DoesNotExist:
            return Response(
                {'valid': False, 'error': 'Certificat invalide ou introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )