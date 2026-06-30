from django.contrib.auth.models import User, Group
from rest_framework import permissions, viewsets
from api.models import Task
from api.serializers import UserSerializer, GroupSerializer, TaskSerializer
from rest_framework import filters

class IsOwner(permissions.BasePermission):
    """
    Permiso personalizado que permite a los usuarios interactuar 
    únicamente con las tareas de las que son propietarios.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

# ViewSets para los modelos User, Group y Task
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
   
# ViewSet para el modelo Task con filtros de búsqueda y ordenamiento     
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['fecha_creacion', 'titulo']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(owner=user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        