import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView,UpdateView,DeleteView,View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test,login_required
from django.urls import reverse_lazy
from .models import Movimiento,Category
from .forms import MovimientoForm
from users.user_permissions import rol_usuario
from datetime import date

class ListarMovimiento(LoginRequiredMixin,UserPassesTestMixin,ListView):
    login_url = '/login/'
    model = Movimiento
    context_object_name = "movimientos"
    template_name = "finansas/listar-movimientos.html"

    def get_queryset(self):
        year_to_filter = date.today().year
        queryset = super().get_queryset()  # Obtiene el queryset original
        return queryset.filter(user=self.request.user,fecha__year=year_to_filter)  # Aplica el filtro deseado
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context
    def test_func(self):
        return rol_usuario(self.request.user)

class CrearMovimiento(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    login_url = '/login/'
    model = Movimiento
    form_class = MovimientoForm
    template_name = "finansas/crear-movimiento.html"
    success_url = reverse_lazy("finansas:listar_mov")
    
    def form_valid(self, form):
        usuario = self.request.user
        form.instance.user = usuario
        return super().form_valid(form)
    
    def test_func(self):
        return rol_usuario(self.request.user)
    
class UpdateMovimiento(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = '/login/'
    model = Movimiento
    form_class = MovimientoForm
    template_name = "finansas/actualizar-movimiento.html"
    success_url = reverse_lazy("finansas:listar_mov")

    def test_func(self):
        return rol_usuario(self.request.user)

class DeleteMovimiento(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = '/login/'
    model = Movimiento
    success_url = reverse_lazy("finansas:listar_mov")

    def test_func(self):
        return rol_usuario(self.request.user)
    


@user_passes_test(rol_usuario, login_url='/login/')
@login_required
def get_category(request):
    id = request.GET.get('id','')
    result = list(Category.objects.filter(tipo_id=int(id)).values('id','name'))
    return HttpResponse(json.dumps(result), content_type="application/json")

