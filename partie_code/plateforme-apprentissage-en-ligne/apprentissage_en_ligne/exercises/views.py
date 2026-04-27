from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Exercice, Soumission
from .serializers import (
    ExerciceSerializer,
    ExerciceCreateSerializer,
    SoumissionSerializer,
    SoumissionCreateSerializer
)
from users.permissions import IsEnseignant, IsApprenant


class ExerciceListView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsEnseignant()]

    def get(self, request):
        cours_id = request.query_params.get('cours')
        exercices = Exercice.objects.all()
        if cours_id:
            exercices = exercices.filter(cours_id=cours_id)
        serializer = ExerciceSerializer(exercices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExerciceCreateSerializer(data=request.data)
        if serializer.is_valid():
            exercice = serializer.save()
            return Response(
                ExerciceSerializer(exercice).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ExerciceDetailView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsEnseignant()]

    def get_object(self, pk):
        try:
            return Exercice.objects.get(pk=pk)
        except Exercice.DoesNotExist:
            return None

    def get(self, request, pk):
        exercice = self.get_object(pk)
        if not exercice:
            return Response(
                {'error': 'Exercice introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(ExerciceSerializer(exercice).data)

    def put(self, request, pk):
        exercice = self.get_object(pk)
        if not exercice:
            return Response(
                {'error': 'Exercice introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ExerciceCreateSerializer(
            exercice, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(ExerciceSerializer(exercice).data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        exercice = self.get_object(pk)
        if not exercice:
            return Response(
                {'error': 'Exercice introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        exercice.delete()
        return Response(
            {'message': 'Exercice supprimé ✅'},
            status=status.HTTP_204_NO_CONTENT
        )


class SoumissionView(APIView):
    """Apprenant submits an answer to an exercise"""
    permission_classes = [IsAuthenticated, IsApprenant]

    def post(self, request, pk):
        exercice = Exercice.objects.filter(pk=pk).first()
        if not exercice:
            return Response(
                {'error': 'Exercice introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )

        # check already submitted
        if Soumission.objects.filter(
            exercice=exercice,
            apprenant=request.user.apprenant
        ).exists():
            return Response(
                {'error': 'Vous avez déjà soumis une réponse pour cet exercice'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SoumissionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        reponse = serializer.validated_data['reponse']

        # check if correct
        is_correct = reponse.strip().lower() == \
                     exercice.reponse_correcte.strip().lower()
        score      = 1.0 if is_correct else 0.0

        soumission = Soumission.objects.create(
            exercice=exercice,
            apprenant=request.user.apprenant,
            reponse=reponse,
            score=score,
            is_correct=is_correct
        )

        return Response({
            'message':    'Réponse soumise ✅' if is_correct else 'Réponse incorrecte ❌',
            'is_correct': is_correct,
            'score':      score,
            'reponse_correcte': exercice.reponse_correcte if not is_correct else None,
            'soumission': SoumissionSerializer(soumission).data
        }, status=status.HTTP_201_CREATED)


class MySoumissionsView(APIView):
    """Get all submissions of the apprenant"""
    permission_classes = [IsAuthenticated, IsApprenant]

    def get(self, request):
        soumissions = Soumission.objects.filter(
            apprenant=request.user.apprenant
        )
        serializer = SoumissionSerializer(soumissions, many=True)
        return Response(serializer.data)