from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    ##Me permite ver el nombre cuando registre algo en el admin de django
    def __str__(self):
        return self.nombre
    
class Aro(models.Model):    
    Aro = models.CharField(max_length=5)
    
    def __str__(self):
        return self.Aro
     
class Genero(models.Model):
    Genero = models.CharField(max_length=50)
    
    def __str__(self):
        return self.Genero

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    aro = models.ForeignKey(Aro,on_delete=models.PROTECT)
    genero = models.ForeignKey(Genero,null=True,on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    modelo = models.CharField(max_length=50)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to="productos", null=True)

    def __str__(self):
        return self.nombre

class CustomUser(AbstractUser):
    Perfiles =(
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
        ('bodeguero', 'Bodeguero'),
    )

    perfil = models.CharField(max_length=15, choices=Perfiles,default='cliente')
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',  # Agregar related_name único
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',  # Agregar related_name único
        related_query_name='customuser'
    )

class Carrito(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)

    def __str__(self):
        return f"Carrito de {self.user.username}"