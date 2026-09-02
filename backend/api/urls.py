from django.urls import path , include 
from rest_framework.routers import DefaultRouter 
from .views import TriggerViewSet,TemplateViewSet, fire_trigger , test_template

router = DefaultRouter()
router.register(r"register", TriggerViewSet)
router.register(r"templates", TemplateViewSet)

urlspatterns = [
    path('', include(router.urls)),
    path('fire/', fire_trigger),
    path('test/<int:template_id>/', test_template)
]