from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser, Marca, Aro, Genero, Producto
from .forms import CustomUserAdminForm

# Register your models here.



class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
#Todos los campos que se pueden manipular en el admin de django
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
#    add_fieldsets = (
#        (None, {
#            'classes': ('wide',),
#            'fields': ('username', 'password1', 'password2', 'perfil'),
#        })),
    #Campos editables de Usuario
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'perfil')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    #Para elegir que campo quiero que se muestre en la tabla de django admin/
    list_display = ["username", "email", "perfil"]

class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "precio", "marca"]
    search_fields   = ["nombre"]
    list_filter     = ["marca"]
    list_per_page   = 5



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Marca)
admin.site.register(Aro)
admin.site.register(Genero)
admin.site.register(Producto,ProductoAdmin)