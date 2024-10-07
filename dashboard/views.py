from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Sum, Case, When, Value, DecimalField
from django.db.models.functions import TruncMonth, ExtractMonth
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from users.user_permissions import rol_usuario
from finansas.models import Movimiento, Tipo
import calendar
import locale
import json
from datetime import date

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


class DashBoard(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "/login/"
    template_name = "dashboard/dasboard.html"

    def get(self, request):

        year_to_filter = date.today().year
        tipo_ingreso = Tipo.objects.get(name="Ingreso").id
        tipo_gasto = Tipo.objects.get(name="Gasto").id
        
        ingresos = (
            Movimiento.objects.filter(
                user=self.request.user, tipo=tipo_ingreso,fecha__year=year_to_filter
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )
        gastos = (
            Movimiento.objects.filter(
                user=self.request.user, tipo=tipo_gasto,fecha__year=year_to_filter
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )
        ahorro = ingresos - gastos

        result_gra_mes = (
            Movimiento.objects.filter(user=self.request.user,fecha__year=year_to_filter)
            .annotate(
                month=TruncMonth("fecha"),
                month_number=ExtractMonth("fecha"),
            )
            .values("month", "month_number")
            .annotate(
                gasto=Sum(
                    Case(
                        When(tipo__name="Gasto", then="amount"),
                        default=Value(0),
                        output_field=models.DecimalField(),
                    )
                ),
                ingreso=Sum(
                    Case(
                        When(tipo__name="Ingreso", then="amount"),
                        default=Value(0),
                        output_field=models.DecimalField(),
                    )
                ),
            )
            .order_by("month")
        )

        resultados_con_nombres = []
        for resultado in result_gra_mes:
            month_number = resultado["month_number"]
            month_name = calendar.month_name[month_number] 

            resultados_con_nombres.append(
                {
                    "month": resultado["month"],
                    "month_name": month_name,
                    "gasto": resultado["gasto"],
                    "ingreso": resultado["ingreso"],
                    "ahorro": resultado["ingreso"]
                    - resultado["gasto"],  
                }
            )

        category_amounts = (
            Movimiento.objects.filter(user=self.request.user, tipo=tipo_gasto,fecha__year=year_to_filter)
            .values("category__name")
            .annotate(gastos=Sum("amount"))
        )

     
        category_percentages = [
            {
                "category": item["category__name"],
                "total_amount": item["gastos"],
                "porcentage": (item["gastos"] / gastos * 100) if gastos > 0 else 0,
            }
            for item in category_amounts
        ]

        category_mes_total_amount = (
            Movimiento.objects.filter(user=self.request.user, tipo=tipo_gasto,fecha__year=year_to_filter)
            .annotate(
                month=TruncMonth("fecha"),
                month_number=ExtractMonth("fecha"),
            )
            .values("month", "month_number", "category__name")
            .annotate(
                gasto=Sum(
                    Case(
                        When(tipo__name="Gasto", then="amount"),
                        default=Value(0),
                        output_field=DecimalField(),
                    )
                ),
            )
            .order_by("month")
        )

        totales_por_categoria = {}

        resultados_category_names = []
        for resultado in category_mes_total_amount:
            category = resultado["category__name"]
            month_number = resultado["month_number"]
            month_name = calendar.month_name[month_number] 

            resultados_category_names.append(
                {
                    "category": category,
                    "month_name": month_name,
                    "gasto": resultado["gasto"],
                }
            )

            if category not in totales_por_categoria:
                totales_por_categoria[category] = 0
            totales_por_categoria[category] += resultado["gasto"]

        unique_months_gastos = sorted(set(
            item["month_name"] for item in resultados_category_names
        ))

        unique_categories = set(item["category"] for item in resultados_category_names)

        

        return render(
            request,
            self.template_name,
            {
                "salario": ingresos,
                "gastos": gastos,
                "ahorro": ahorro,
                "grafico_mensual": json.dumps(
                    resultados_con_nombres, cls=DjangoJSONEncoder
                ),
                "category_porcentajes": json.dumps(
                    category_percentages, cls=DjangoJSONEncoder
                ),
                "resultados_category_names": resultados_category_names,
                "unique_months_gastos": unique_months_gastos,
                "unique_categories": unique_categories,
                "totales_por_categoria": totales_por_categoria,
            },
        )

    def test_func(self):
        return rol_usuario(self.request.user)
