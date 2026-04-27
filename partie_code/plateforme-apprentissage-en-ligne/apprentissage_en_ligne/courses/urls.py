from django.urls import path
from . import views

urlpatterns = [
    path('modules/',                  views.ModuleListView.as_view(),      name='module-list'),
    path('modules/<int:pk>/',         views.ModuleDetailView.as_view(),    name='module-detail'),
    path('modules/<int:pk>/courses/', views.ModuleCoursListView.as_view(), name='module-cours'),
    path('',                          views.CoursListView.as_view(),       name='cours-list'),
    path('<int:pk>/',                 views.CoursDetailView.as_view(),     name='cours-detail'),
]