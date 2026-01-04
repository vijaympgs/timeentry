from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.customer import CustomerViewSet, LeadViewSet, ContactViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'leads', LeadViewSet)
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('crm/', include(router.urls)),
]
