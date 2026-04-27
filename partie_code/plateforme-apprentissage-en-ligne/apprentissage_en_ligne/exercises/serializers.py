from rest_framework import serializers
from .models import Exercice, Soumission


class ExerciceSerializer(serializers.ModelSerializer):
    cours_titre = serializers.SerializerMethodField()

    class Meta:
        model  = Exercice
        fields = [
            'id', 'cours_titre', 'type',
            'enonce', 'difficulte', 'score_minimum'
        ]

    def get_cours_titre(self, obj):
        return obj.cours.titre


class ExerciceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Exercice
        fields = [
            'cours', 'type', 'enonce',
            'reponse_correcte',
            'difficulte', 'score_minimum'
        ]


class SoumissionSerializer(serializers.ModelSerializer):
    exercice_enonce = serializers.SerializerMethodField()
    apprenant_nom   = serializers.SerializerMethodField()

    class Meta:
        model  = Soumission
        fields = [
            'id', 'exercice', 'exercice_enonce',
            'apprenant_nom', 'reponse',
            'score', 'is_correct', 'date'
        ]

    def get_exercice_enonce(self, obj):
        return obj.exercice.enonce

    def get_apprenant_nom(self, obj):
        return str(obj.apprenant.utilisateur)


class SoumissionCreateSerializer(serializers.Serializer):
    reponse = serializers.CharField()

    def validate_reponse(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                'La réponse ne peut pas être vide'
            )
        return value