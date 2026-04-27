from django.urls import path
from . import views

urlpatterns = [
    # enrollment
    path('enroll/',                        views.EnrollView.as_view(),              name='enroll'),
    path('my-inscriptions/',               views.MyInscriptionsView.as_view(),      name='my-inscriptions'),
    path('my-inscriptions/<int:pk>/',      views.InscriptionDetailView.as_view(),   name='inscription-detail'),

    # certifications
    path('my-certifications/',             views.MyCertificationsView.as_view(),    name='my-certifications'),
    path('download/<int:pk>/',             views.DownloadCertificateView.as_view(), name='download-certificate'),
    path('verify/<str:code>/',             views.VerifyCertificationView.as_view(), name='verify-certification'),
]