from django.contrib import admin

from appcadenadealimentos.models import Empresa,Empleado,Usuario,Movimientos
admin.site.register(Empresa)
admin.site.register(Empleado)
admin.site.register(Usuario)
admin.site.register(Movimientos)