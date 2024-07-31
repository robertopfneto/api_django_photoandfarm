from django.db import models
from django.utils.timezone import now

class Farm(models.Model):
    name = models.CharField(max_length=50)
    rua = models.CharField(max_length=50) 
    numero = models.IntegerField (null=False) 
    bairro = models.CharField(max_length=50)  

    class Meta: 
        db_table = 'Farm'
        ordering = ['id']
        
class Person(models.Model):
    name = models.CharField(max_length=50, null= False)
    cpf = models.CharField(max_length=11, null = False)
    fk_farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'Person'
        ordering = ['id']
    
class Photo(models.Model):
    name = models.CharField(max_length=90,null=False)
    created_at = models.DateTimeField(default=now)
    image = models.ImageField(upload_to='photos/', null=True, blank=True)
    fk_farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True)
    fk_person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'Photo'
