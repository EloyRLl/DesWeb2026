# Django imports
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
import random
import time

# Django REST Framework & Knox imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

"""
Código  Nombre  Uso típico
200 OK  Petición exitosa (valor por defecto).
201 Created Se ha creado un recurso (ej. un nuevo usuario).
400 Bad Request Datos enviados inválidos o mal formateados.
401 Unauthorized    El usuario no está autenticado.
403 Forbidden   Autenticado, pero sin permisos para esa acción.
404 Not Found   El recurso solicitado no existe.
500 Internal Server Error   Error inesperado en tu código Python.
"""

# ✅ ESTA ES LA FUNCIÓN BUENA PARA ANGULAR Y KNOX
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_logged_in(request):
    return Response({
        "is_logged_in": True,
        "username": request.user.username
    })

# --- EL RESTO DE TUS VISTAS CLÁSICAS ---

def custom_logout_view(request):
    logout(request)
    return redirect("/accounts/login/")

def notLoggedIn(request):
    return JsonResponse({"ok":False,"message": "You are not logged in", "data":[]},status=400)

class HelloWord(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Core. Hello world", "data":[]},status=200)

class LoginView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            username=request.user.username
            return JsonResponse({"ok":True,"message": "The user {0} already is authenticated".format(username), "data":[{'username':request.user.username}]}, status=200)

        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            login(request,user)
            return JsonResponse({"ok":True,"message": "User {0} logged in".format(username), "data":[{"username": username}]}, status=200)
        else:
            seconds=random.uniform(0, 1)
            time.sleep(seconds)
            return JsonResponse({"ok":False,"message": "Wrong user or password", "data":[]},status=400)

class LogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username=request.user.username
        logout(request) 
        return JsonResponse({"ok":True,"message": "The user {0} is now logged out".format(username), "data":[]}, status=200)

# ❌ He comentado esta clase antigua para que no choque con la función buena de arriba
# Si la estabas usando en algún sitio, puedes descomentarla, pero asegúrate de no mezclarla en el urls.py
# class IsLoggedIn(View):
#     def post(self, request, *args, **kwargs):
#         ...