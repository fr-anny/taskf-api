from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    completado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(
        User,
        related_name="tasks",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo