from django.contrib.auth import get_user_model
from finansas.models import Category,Tipo
User = get_user_model()

def create_initial_data():
    if len(User.objects.filter(username="admin"))==0:
        User.objects.create_superuser(username="admin", password="admin" , email='admin@lol.cl')
    if len(User.objects.filter(username="Juan"))==0:
        User.objects.create_user(username="Juan", password="Juan123456" , email='juan@lol.cl')
    if len(User.objects.filter(username="Pedro"))==0:
        User.objects.create_user(username="Pedro", password="Pedro123456" , email='pedro@lol.cl')
    if len(User.objects.filter(username="Catalina"))==0:
        User.objects.create_user(username="Catalina", password="Catalina123456" , email='cata@lol.cl')

    if len(Tipo.objects.filter(name='Gasto')) == 0:
        Tipo.objects.create(name='Gasto')
    if len(Tipo.objects.filter(name='Ingreso'))== 0:
        Tipo.objects.create(name='Ingreso')

    gastos = [
        "Alimentacion",
        "Vestimenta",
        "Educacion",
        "Gastos Comunes",
        "Salud",
        "Transporte",
        "Ocio",
        "Otros",
    ]
    
    ingresos=  ["Remuneracion","Venta", "Otros"]


    for category_name in gastos:
        tipo_instance = Tipo.objects.get(name='Gasto')
        if not Category.objects.filter(name=category_name,tipo=tipo_instance).exists():
            Category.objects.create(name=category_name, tipo=tipo_instance)

    for category_name in ingresos:
       
        tipo_instance = Tipo.objects.get(name='Ingreso')
        print(f'category_name {category_name} ?: {Category.objects.filter(name=category_name,tipo=tipo_instance).exists()}')
        if not Category.objects.filter(name=category_name,tipo=tipo_instance).exists():
            Category.objects.create(name=category_name, tipo=tipo_instance)
