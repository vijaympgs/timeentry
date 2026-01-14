"""
Profile View URL Configuration - Layer 3: Experience/Enrichment Layer
URL patterns for employee profile, skills, certifications, and career development APIs
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for Profile View endpoints
router = DefaultRouter()
router.register(r'profiles', views.EmployeeProfileViewSet, basename='profile')
router.register(r'skills', views.SkillViewSet, basename='skill')
router.register(r'certifications', views.CertificationViewSet, basename='certification')
router.register(r'languages', views.LanguageViewSet, basename='language')
router.register(r'learning-paths', views.LearningPathViewSet, basename='learning-path')
router.register(r'aspirations', views.AspirationViewSet, basename='aspiration')

# URL patterns for Profile View module
urlpatterns = [
    path('api/v1/', include(router.urls)),
]
