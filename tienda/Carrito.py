from .models import Carrito

class CarritoManager:
    def __init__(self, request):
        self.request = request
        if request.user.is_authenticated:
            self.carrito, created = Carrito.objects.get_or_create(user=request.user)
        else:
            self.session = request.session
            carrito = self.session.get("carrito")
            if not carrito:
                self.session["carrito"] = {}
                self.carrito = self.session["carrito"]
            else:
                self.carrito = carrito

    def agregar(self, producto):
        if self.request.user.is_authenticated:
            self.carrito.productos.add(producto)
        else:
            id = str(producto.id)
            if id not in self.carrito.keys():
                self.carrito[id]={
                    "producto_id"   : producto.id,
                    "nombre"        : producto.nombre,
                    "acumulado"     : producto.precio,
                    "cantidad"      : 1
                }
            else:
                self.carrito[id]["cantidad"] += 1
                self.carrito[id]["acumulado"] += producto.precio
        self.guardar_carrito()

    def guardar_carrito(self):
        if self.request.user.is_authenticated:
            self.carrito.save()
        else:
            self.session["carrito"] = self.carrito
            self.session.modified = True
    
    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        id = str(producto.id)
        if hasattr(self.carrito, 'keys'):
            if id in self.carrito.keys():
                self.carrito[id]["cantidad"] -= 1
                self.carrito[id]["acumulado"] -= producto.precio
                if self.carrito[id]["cantidad"] <= 0:
                    self.eliminar(producto)
                self.guardar_carrito()
        else:
            if id in self.carrito:
                self.carrito[id]["cantidad"] -= 1
                self.carrito[id]["acumulado"] -= producto.precio
                if self.carrito[id]["cantidad"] <= 0:
                    self.eliminar(producto)
                self.guardar_carrito()
    
    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True