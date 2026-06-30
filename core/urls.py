from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.http import JsonResponse

from api.views import (
    UserViewSet,
    GroupViewSet,
    TaskViewSet
)

def health(request):
    return JsonResponse({"status": "ok"})

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('health/', health),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

