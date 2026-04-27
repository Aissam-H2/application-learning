from django.urls import path
from . import views

urlpatterns = [
    # exercises
    path('',               views.ExerciceListView.as_view(),   name='exercice-list'),
    path('<int:pk>/',      views.ExerciceDetailView.as_view(), name='exercice-detail'),

    # submissions
    path('<int:pk>/submit/', views.SoumissionView.as_view(),   name='soumission'),
    path('my-submissions/',  views.MySoumissionsView.as_view(),name='my-soumissions'),
]