from rest_framework import serializers
from .models import Inscription, Certification
from courses.serializers import CoursSerializer # pyright: ignore[reportMissingImports]


class InscriptionSerializer(serializers.ModelSerializer):
    cours_detail    = CoursSerializer(source='cours', read_only=True)
    apprenant_nom   = serializers.SerializerMethodField()

    class Meta:
        model  = Inscription
        fields = [
            'id', 'apprenant_nom', 'cours',
            'cours_detail', 'date_inscription',
            'progression', 'is_completed'
        ]

    def get_apprenant_nom(self, obj):
        return str(obj.apprenant.utilisateur)


class InscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Inscription
        fields = ['cours']

    def create(self, validated_data):
        apprenant = self.context['request'].user.apprenant
        cours     = validated_data['cours']

        if Inscription.objects.filter(
            apprenant=apprenant, cours=cours
        ).exists():
            raise serializers.ValidationError(
                'Vous êtes déjà inscrit à ce cours'
            )

        return Inscription.objects.create(
            apprenant=apprenant,
            cours=cours
        )


class CertificationSerializer(serializers.ModelSerializer):
    apprenant_nom = serializers.SerializerMethodField()
    cours_titre   = serializers.SerializerMethodField()

    class Meta:
        model  = Certification
        fields = [
            'id', 'apprenant_nom', 'cours_titre',
            'date_emission', 'code_validation'
        ]

    def get_apprenant_nom(self, obj):
        return str(obj.inscription.apprenant.utilisateur)

    def get_cours_titre(self, obj):
        return obj.inscription.cours.titre