
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegisterUserForm

def registro(request):
    context = {
        'form': RegisterUserForm()
    }
    
    if request.method == 'POST':
        form = RegisterUserForm(data=request.POST)
        
        if form.is_valid():
            user = form.save() 
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('dashboard:dashboard')
            else:
                messages.error(request, 'Error en la autenticación. Intente nuevamente.')
        else:
            context['form'] = form
            
    return render(request, 'registration/registro.html', context)
