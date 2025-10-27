from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def loguearse(request):
    if request.method == "POST":
        nombre=request.POST['username']
        contrasena=request.POST['password']
        usuario = authenticate(request, username=nombre, password=contrasena)

        if usuario is not None:
            login(request, usuario)
            return redirect('e_destacado')
        
        else:
            messages.success(request, ("Hubo un error, intenta de nuevo"))
            return redirect('login')
        
    else:
        return render(request, 'usuarios/login.html', {})
    

def salir(request):
    logout(request)
    messages.success(request, ("Saliste de tu cuenta"))
    return redirect('e_destacado')

def registrar(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            nombre=form.cleaned_data['username']
            contrasena=form.cleaned_data['password1']
            usuario= authenticate(username=nombre, password=contrasena)
            login(request, usuario)
            messages.success(request, ("Cuenta exitosamente creada"))
            return redirect('e_destacado')
    else:
        form=UserCreationForm()

    return render(request, 'usuarios/registrar.html', {'form':form,})
