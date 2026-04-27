from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Cours, Module
from .serializers import CoursSerializer, CoursCreateSerializer, ModuleSerializer
from users.permissions import IsEnseignant # pyright: ignore[reportMissingImports]


class ModuleListView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsEnseignant()]

    def get(self, request):
        modules    = Module.objects.all()
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ModuleDetailView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsEnseignant()]

    def get_object(self, pk):
        try:
            return Module.objects.get(pk=pk)
        except Module.DoesNotExist:
            return None

    def get(self, request, pk):
        module = self.get_object(pk)
        if not module:
            return Response(
                {'error': 'Module introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(ModuleSerializer(module).data)

    def put(self, request, pk):
        module = self.get_object(pk)
        if not module:
            return Response(
                {'error': 'Module introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ModuleSerializer(
            module, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        module = self.get_object(pk)
        if not module:
            return Response(
                {'error': 'Module introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        module.delete()
        return Response(
            {'message': 'Module supprimé ✅'},
            status=status.HTTP_204_NO_CONTENT
        )


class CoursListView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsEnseignant()]

    def get(self, request):
        niveau = request.query_params.get('niveau')
        search = request.query_params.get('search')
        cours  = Cours.objects.all()
        if niveau:
            cours = cours.filter(niveau_difficulte=niveau)
        if search:
            cours = cours.filter(titre__icontains=search)
        serializer = CoursSerializer(cours, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CoursCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            cours = serializer.save()
            return Response(
                CoursSerializer(cours).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CoursDetailView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsEnseignant()]

    def get_object(self, pk):
        try:
            return Cours.objects.get(pk=pk)
        except Cours.DoesNotExist:
            return None

    def get(self, request, pk):
        cours = self.get_object(pk)
        if not cours:
            return Response(
                {'error': 'Cours introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(CoursSerializer(cours).data)

    def put(self, request, pk):
        cours = self.get_object(pk)
        if not cours:
            return Response(
                {'error': 'Cours introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        if cours.enseignant.utilisateur != request.user:
            return Response(
                {'error': 'Vous n\'êtes pas le propriétaire de ce cours'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CoursCreateSerializer(
            cours, data=request.data, partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            cours = serializer.save()
            return Response(CoursSerializer(cours).data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        cours = self.get_object(pk)
        if not cours:
            return Response(
                {'error': 'Cours introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        if cours.enseignant.utilisateur != request.user:
            return Response(
                {'error': 'Vous n\'êtes pas le propriétaire de ce cours'},
                status=status.HTTP_403_FORBIDDEN
            )
        cours.delete()
        return Response(
            {'message': 'Cours supprimé ✅'},
            status=status.HTTP_204_NO_CONTENT
        )


class ModuleCoursListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            module = Module.objects.get(pk=pk)
        except Module.DoesNotExist:
            return Response(
                {'error': 'Module introuvable'},
                status=status.HTTP_404_NOT_FOUND
            )
        cours      = module.cours.all()
        serializer = CoursSerializer(cours, many=True)
        return Response(serializer.data)