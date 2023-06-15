from django.shortcuts import render,redirect, get_object_or_404
from .models import Producto, CustomUser
from .forms import ProductoForm , CustomUserCreationForm
from .Carrito import CarritoManager
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView

from .models import CustomUser

#Rutas 
def home(request):
    return render(request, "Home/Home.html")

def bodega(request):
    return render(request, "Bodega/Bodega.html")

def cliente(request):
    return render(request, "Cliente/Cliente.html")

def administrador(request):
    return render(request, "Admin/Administrador.html")

def producto(request):
    productos = Producto.objects.all()
    data = {
        'productos' : productos
    }
    return render(request, "Producto/Producto.html", data)


def detalles(request, producto_id):
    #INVESTIGAR ACERCA DE ESTA OPCION
    #producto = get_object_or_404(Producto, id=producto_id)
    producto = Producto.objects.get(id=producto_id)
    data = {'producto' : producto}
    
    return render(request, "Producto/Detalles.html", data)


#CRUD Administrador 
def agregar_producto(request):

    
    data = {
        'form' : ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "guardado correctamente"
        else:
            data["form"] = formulario
            data["mensaje"] = "Error"
    return render(request, "Admin/Agregar.html", data)

def listar_productos(request):
    producto = Producto.objects.all()
    data = {
        "producto" : producto
    }
    return render(request, "Admin/Listar.html", data)

def modificar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    data = {
        'form' : ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_productos")
        else:
            data["form"] = formulario
            data["mensaje"] = "Error"
    return render(request, "Admin/Modificar.html", data)

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id) 
    producto.delete()
    return redirect(to="listar_productos")

#CRUD Carrito
def agregar_producto_carrito(request, producto_id):
    carrito = CarritoManager(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect("Producto")
    
def eliminar_producto_carrito(request, producto_id):
    carrito = CarritoManager(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("Producto")

def restar_producto_carrito(request, producto_id):
    carrito = CarritoManager(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("Producto")

def limpiar_producto_carrito(request):
    carrito = CarritoManager(request)
    carrito.limpiar()
    return redirect("Producto")


#Registros e Inicio de sesión
def registro(request):
    data = {
        'form' : CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Registro Completo")
            return redirect(to="Home")
        data["form"] =formulario
    return render(request, 'registration/Registro.html', data)

class LoginCustom(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        custom_user = CustomUser.objects.get(username=self.request.user.username)
        custom_user = self.request.user
        if hasattr(custom_user, 'perfil'): 
            if custom_user.perfil == 'administrador':
                return '/Administrador/'
            elif custom_user.perfil == 'cliente':
                return '/Cliente/'
            elif custom_user.perfil == 'bodeguero':
                return '/Bodega/'
        return '/'
        
