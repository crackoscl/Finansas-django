
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .forms import RegisterUserForm, ProfileUpdateForm
from .user_permissions import rol_usuario
User = get_user_model()

class EditUser(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    template_name = 'users/actualizar_usuario.html'
    context_object_name = 'user'
    queryset = User.objects.all()
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("dashboard:dashboard")

    def form_valid(self, form):
        # Save the uploaded image
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super(EditUser, self).get_context_data(**kwargs)
    #     user = self.request.user
    #     context['profile_form'] = ProfileUpdateForm(instance=self.request.user.userprofile, initial={'first_name': user.first_name, 'last_name': user.last_name})
    #     return context

    # def form_valid(self, form):
    #     profile = form.save(commit=False)
    #     user = profile.user
    #     user.last_name = form.cleaned_data['last_name']
    #     user.first_name = form.cleaned_data['first_name']
    #     user.save()
    #     profile.save()
       
    
    def test_func(self):
        return rol_usuario(self.request.user)



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
