from django.db import models
from users.models import User


class Tipo(models.Model):
    name = models.CharField(max_length=50)
    creation_date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)
    creation_date = models.DateField(auto_now=True)
    tipo =  models.ForeignKey(Tipo, on_delete=models.CASCADE,related_name='categories')

    def __str__(self) -> str:
        return self.name
    


class  Movimiento(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='movimientos_by_category')
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE,related_name='movimientos_by_tipo')
    fecha = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    note = models.TextField(max_length=200)
    concept =  models.TextField(max_length=500,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='usuario')
 
    class Meta:
        verbose_name_plural = "Movimiento"
        
    

    def __str__(self) -> str:
        return self.tipo
