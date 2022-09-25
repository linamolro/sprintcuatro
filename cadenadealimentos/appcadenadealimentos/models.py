from django.db import models
from datetime import datetime

class Empresa (models.Model):
    codigo_empresa = models.CharField(max_length=9, primary_key=True, unique=True)
    nombre_empresa = models.CharField(max_length=40)
    nit = models.IntegerField()
    nombre_contacto = models.CharField(max_length=40)
    cargo_contacto = models.CharField(max_length=40)
    pais = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=20)
    direccion = models.CharField(max_length=40)
    telefono = models.CharField(max_length=20)
    correo_empresa = models.CharField(max_length=50)

    def __str__(self):
        return '{} {} {}'.format(self.codigo_empresa, self.nit, self.nombre_empresa, self.pais, self.ciudad, self.telefono, self.correo_empresa)

class Empleado (models.Model):
    cedula = models.IntegerField(primary_key=True,unique=True)
    primer_nombre = models.CharField(max_length=10)
    segundo_nombre = models.CharField(max_length=10)
    primer_apellido = models.CharField(max_length=10)
    segundo_apellido = models.CharField(max_length=10)
    codigo_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=40)
    correo_empleado = models.CharField(max_length=50)
    direccion_empleado = models.CharField(max_length=40)
    celular_empleado = models.CharField(max_length=15)
    tipo_contrato = models.CharField(max_length=20)
    profesion = models.CharField(max_length=25)
    banco = models.CharField(max_length=40)

    def __str__(self):
        return '{} {} {}'.format(self.cedula, self.primer_nombre, self.primer_apellido, self.codigo_empresa, self.banco)

class Usuario (models.Model):
    user_name = models.CharField(max_length=10 ,primary_key=True, unique=True)
    cedula = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    user_password = models.CharField(max_length=15)

    class tipo_select(models.TextChoices):
        empleado = 'Empleado',('Empleado')
        administrador = 'Administrador',('Administrador')

    tipo_rol = models.CharField(max_length=15, choices=tipo_select.choices)
    data_create = models.DateField(default=datetime.now, blank=False)

    def __str__(self):
        return '{} {} {}'.format(self.user_name, self.tipo_rol)

class Movimientos (models.Model):
    id_registro = models.CharField(max_length=7,primary_key=True)
    codigo_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    valor = models.IntegerField()
    
    class tipo_select (models.TextChoices):
        ingreso ='Ing',('Ingresos')
        egreso = 'Egr',('Egreso')

    tipo_movimiento = models.CharField(max_length=3,choices=tipo_select.choices)
    movimiento_fecha = models.DateField()
    user_name = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {} {}'.format(self.codigo_empresa, self.user_name, self.valor, self.tipo_movimiento, self.movimiento_fecha)


