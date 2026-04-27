from rest_framework.permissions import BasePermission


class IsEnseignant(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'enseignant')
        )


class IsApprenant(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'apprenant')
        )


class IsAdministrateur(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'administrateur')
        )


class IsEnseignantOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'enseignant')
        )