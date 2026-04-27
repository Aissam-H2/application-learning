from rest_framework import serializers
from .models import Cours, Module


class CoursSerializer(serializers.ModelSerializer):
    enseignant_nom = serializers.SerializerMethodField()

    class Meta:
        model  = Cours
        fields = [
            'id', 'titre', 'description',
            'niveau_difficulte', 'duree',
            'enseignant_nom', 'module'
        ]

    def get_enseignant_nom(self, obj):
        return str(obj.enseignant.utilisateur)


class CoursCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Cours
        fields = [
            'titre', 'description',
            'niveau_difficulte', 'duree',
            'module'
        ]

    def create(self, validated_data):
        enseignant = self.context['request'].user.enseignant
        return Cours.objects.create(
            enseignant=enseignant,
            **validated_data
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ModuleSerializer(serializers.ModelSerializer):
    cours       = CoursSerializer(many=True, read_only=True)
    total_cours = serializers.SerializerMethodField()

    class Meta:
        model  = Module
        fields = [
            'id', 'titre', 'type_contenu',
            'contenu', 'order',
            'total_cours', 'cours'
        ]

    def get_total_cours(self, obj):
        return obj.cours.count()