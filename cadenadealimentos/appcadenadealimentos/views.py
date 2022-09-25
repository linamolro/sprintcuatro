import json
from django.shortcuts import render, redirect
from email import message
from django.views import View
from .models import Empresa, Empleado, Usuario, Movimientos
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

#Vista de Empresa
class EmpresaViews(View):
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def post(self,request):
        datos = json.loads(request.body)
        Empresa.objects.create(codigo_empresa=datos["codigo_empresa"],nombre_empresa=datos["nombre_empresa"],nit=datos["nit"],nombre_contacto=datos["nombre_contacto"],cargo_contacto=datos["cargo_contacto"],pais=datos["pais"],ciudad=datos["ciudad"],direccion=datos["direccion"],telefono=datos["telefono"],correo_empresa=datos["correo_empresa"])
        return JsonResponse(datos)

    def get(self,request,name=""):
        if name != "":
            empresa = Empresa.objects.filter(codigo_empresa=name).all()
            if len(empresa)>0:
                empresa_a_consultar = empresa[0]
                datos = {"Empresa": empresa_a_consultar}
            else:
                datos = {"Respuesta":"Registro no encontrado"}
        else:
            template_name = "consultarempresa.html"
            empresa = Empresa.objects.all()
            datos = {'listadoempresas':empresa}
        return render(request,template_name,datos)

    def put (self, request, nomb):
        datos = json.loads(request.body)
        emp = list(Empresa.objects.filter(codigo_empresa=nomb).values())
        if len(emp)>0:
            Empresas = Empresa.objects.get(codigo_empresa=nomb)
            Empresas.nombre_empresa=datos['nombre_empresa']
            Empresas.nit=datos['nit']
            Empresas.nombre_contacto=datos['nombre_contacto']
            Empresas.cargo_contacto=datos['cargo_contacto']
            Empresas.pais=datos['pais']
            Empresas.ciudad=datos['ciudad']
            Empresas.direccion=datos['direccion']
            Empresas.telefono=datos['telefono']
            Empresas.correo_empresa=datos['correo_empresa']
            Empresas.save()
            mensaje = {"Repuesta":"Datos Actualizados"}
        else:
            mensaje = {"Repuesta":"Datos no Actualizados"}
        return JsonResponse(mensaje)

    def delete(self, request, nomb):
        emp = list(Empresa.objects.filter(codigo_empresa=nomb).values())
        if len(emp)>0:
            Empresa.objects.filter(codigo_empresa=nomb).delete()
            mensaje = {"Repuesta":"El Registro de Empresa ha Sido Eliminado"}
        else:
            mensaje = {"Repuesta":"Empresa No Encontrada"}
        return JsonResponse(mensaje)

#Vista de Empleado
class EmpleadoViews(View):

    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def post(self, request):
        datos = json.loads(request.body)
        try:
            empresa = Empresa.objects.get(codigo_empresa=datos["codigo_empresa"])
            Empleado.objects.create(cedula=datos["cedula"],primer_nombre=datos["primer_nombre"],segundo_nombre=datos["segundo_nombre"],primer_apellido=datos["primer_apellido"],segundo_apellido=datos["segundo_apellido"],codigo_empresa=empresa,cargo=datos["cargo"],correo_empleado=datos["correo_empleado"],direccion_empleado=datos["direccion_empleado"],celular_empleado=datos["celular_empleado"],tipo_contrato=datos["tipo_contrato"],profesion=datos["profesion"],banco=datos["banco"])
            return JsonResponse(datos) 
        except Empresa.DoesNotExist:
            mensaje = {"Respuesta":"La empresa no existe"}
        return JsonResponse(mensaje)                   

    def put(self, request, cc):
        datos = json.loads(request.body)
        try:
            empleado = list(Empleado.objects.filter(cedula = cc).values())
            if len(empleado)>0:
                empleados = Empleado.objects.get(cedula = cc)
                empleados.primer_nombre = datos["primer_nombre"]
                empleados.segundo_nombre = datos["segundo_nombre"]
                empleados.primer_apellido = datos["primer_apellido"]
                empleados.segundo_apellido = datos["segundo_apellido"]
                empresa = Empresa.objects.get(codigo_empresa=datos["codigo_empresa"])
                empleados.codigo_empresa = empresa
                empleados.cargo = datos["cargo"]
                empleados.correo_empleado = datos["correo_empleado"]
                empleados.direccion_empleado = datos["direccion_empleado"]
                empleados.celular_empleado = datos["celular_empleado"]
                empleados.tipo_contrato = datos["tipo_contrato"]
                empleados.profesion = datos["profesion"]
                empleados.banco = datos["banco"]
                empleados.save()
                mensaje = {"Respuesta":"Datos actualizados"}
            else:
                mensaje = {"Respuesta":"Registro no encontrado"}
            return JsonResponse(mensaje)
        except Empresa.DoesNotExist:
            mensaje = {"Respuesta":"La empresa no existe"}
        return JsonResponse(mensaje)
    
    def get(self,request,cc=0):
        if cc != 0:
            empleado = Empleado.objects.filter(cedula=cc).all()
            if len(empleado)>0:
                empleado_a_consultar = empleado[0]
                datos = {"Empleado": empleado_a_consultar}
            else:
                datos = {"Respuesta":"Registro no encontrado"}
        else:
            template_name = "consultarempleado.html"
            empleado = Empleado.objects.all()
            datos = {'listadoempleados':empleado}
        return render(request,template_name,datos)

    def delete(self, request, cc):
        empleado = list(Empleado.objects.filter(cedula=cc).values())
        if len(empleado)>0:
            Empleado.objects.filter(cedula=cc).delete()
            mensaje = {"Respuesta":"Registro eliminado"}
        else:
            mensaje = {"Respuesta":"Registro no encontrado"}
        return JsonResponse(mensaje)

#Vista de Usuario
class UsuarioViews(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        datosUsuarios = json.loads(request.body)
        try:
            empleado = Empleado.objects.get(cedula = datosUsuarios["cedula"])
            Usuario.objects.create(user_name=datosUsuarios["user_name"], cedula=empleado,
                               user_password=datosUsuarios["user_password"], tipo_rol=datosUsuarios["tipo_rol"],
                               data_create=datosUsuarios["data_create"])
            return JsonResponse(datosUsuarios)
        except Empleado.DoesNotExist:
            mensaje = {"Respuesta":"El empleado no existe"}
            return JsonResponse(mensaje)

    def put(self, request, user):
        datosUsuarios = json.loads(request.body)
        usuario = list(Usuario.objects.filter(user_name=user).values())
        if len(usuario) > 0:
            usuario = Usuario.objects.get(user_name=user)
            usuario.user_password = datosUsuarios["user_password"]
            usuario.save()
            mensaje = {"Respuesta": "Datos actualizados"}
        else:
            mensaje = {"Respuesta": "Registro no econtrado"}
        return JsonResponse(mensaje)                    
    
    def get(self, request, user=""):
        if user != "":
            usuario = list(Usuario.objects.filter(user_name = user).values())
            if len(usuario)>0:
                buscar_usuario = usuario[0]
                datosUsuarios = {"Usuario": buscar_usuario}
            else:
                datosUsuarios = {"Respuesta": "Registro no encontrado"}
        else:
            usuario = list(Usuario.objects.values())
            datosUsuarios = {'Listado de usuarios':usuario}
        return JsonResponse(datosUsuarios)

    def delete(self,request, user):
        usuario = list(Usuario.objects.filter(user_name = user).values)
        if len(usuario)>0:
            usuario.objects.filter(user_name=user).delete()
            mensaje = {"Respuesta":"Registro eliminado"}
        else:
            mensaje = {"Respuesta":"Registro no encontrado"}
        return JsonResponse(mensaje)      

#Vista de modificación usuario datos empleado
class UsuarioEmpleadoViews(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def put(self, request, cc):
        datos = json.loads(request.body)
        empleado = list(Empleado.objects.filter(cedula = cc).values())
        if len(empleado)>0:
            empleados = Empleado.objects.get(cedula = cc)
            empleados.primer_nombre = datos["primer_nombre"]
            empleados.segundo_nombre = datos["segundo_nombre"]
            empleados.primer_apellido = datos["primer_apellido"]
            empleados.segundo_apellido = datos["segundo_apellido"]
            empleados.correo_empleado = datos["correo_empleado"]
            empleados.direccion_empleado = datos["direccion_empleado"]
            empleados.celular_empleado = datos["celular_empleado"]
            empleados.profesion = datos["profesion"]
            empleados.banco = datos["banco"]
            empleados.save()
            mensaje = {"Respuesta":"Datos actualizados"}
        else:
            mensaje = {"Respuesta":"Registro no encontrado"}
        return JsonResponse(mensaje)

#Vista de movimientos
class MovimientosViews(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, nomb=""):
        if nomb =="":
            emp = list(Movimientos.objects.values())
            datos = {'Movimientos empresa':emp}
        else:
            emp = list(Movimientos.objects.filter(codigo_empresa=nomb).values())
            if len(emp)>0:
                EmpNomb = emp[0]
                datos={"Empresa Movimiento":emp}
            else:
                datos={"respuesta":"Empresa Movimiento no Encontrado"}                   
        return JsonResponse(datos)    
    
    def post(self,request):
        datos = json.loads(request.body)
        try:
            emp = Empresa.objects.get(codigo_empresa=datos["codigo_empresa"])
            usu = Usuario.objects.get(user_name = datos["user_name"])
            Movimientos.objects.create(id_registro=datos["id_registro"],codigo_empresa=emp,
            valor = datos["valor"],
            tipo_movimiento = datos["tipo_movimiento"],
            movimiento_fecha = datos["movimiento_fecha"],
            user_name = usu)
            return JsonResponse(datos)
        except Empresa.DoesNotExist:
            mensaje = {"Respuesta":"La empresa no existe"}
            return JsonResponse(mensaje) 
        except Usuario.DoesNotExist:
            mensaje = {"Respuesta":"El usuario no existe"}
            return JsonResponse(mensaje)

#Inicio de sesión
def loginusuario(request):
    if request.method=='POST':
        try:
            datosUsuario = Usuario.objects.get(user_name=request.POST['user_name'],user_password=request.POST['user_password'])
            if datosUsuario.tipo_rol == "Administrador":
                request.session['user_name']=datosUsuario.user_name
                return render(request, 'administrador.html')
            elif datosUsuario.tipo_rol == "Empleado":
                request.session['user_name']=datosUsuario.user_name
                return render(request, 'empleado.html')
        except Usuario.DoesNotExist:
            return(message.success(request, "No existe"))
    return render(request, 'login.html')