from typing import Any
from django import forms
from .models import Movimiento, Category, Tipo
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ["tipo", "category", "fecha","amount", "note", "concept"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            'fecha': forms.DateInput(format=('%Y-%m-%d'),attrs={
                'class': 'form-control',  # Clase para Bootstrap
                'id': 'fecha',            # ID para el selector
                'placeholder': 'Selecciona una fecha',
                'type': 'date'            # Esto permite que el navegador muestre un selector de fecha
            }),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "note": forms.Textarea(attrs={"class": "form-control"}),
            "concept": forms.Textarea(attrs={"class": "form-control"}),
        }


        error_messages = {
            "category": {
                "required": "Por favor, selecciona una opcion.",
                "invalid": "",
            },
            "tipo": {
                "required": "Por favor, selecciona una opcion.",
                "invalid": "",
            },
            "fecha": {
                "required": "Por favor, seleccione una fecha",
                "invalid": "",
            },
            "note": {
                "required": "Por favor, ingresa una nota.",
                "invalid": "",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['fecha'].initial = timezone.now().date()
        self.fields["category"].queryset = Category.objects.none()
        if "tipo" in self.data:
            try:
                tipo_id = int(self.data.get("tipo"))
                self.fields["category"].queryset = Category.objects.filter(
                    tipo_id=tipo_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["category"].queryset = Category.objects.filter(tipo=self.instance.tipo).order_by("name")


    def clean_amount(self):
        numero = self.cleaned_data.get("amount")
        if numero <= 0:
            raise forms.ValidationError(
                "El número debe ser positivo y no puede ser cero."
            )
        return numero
