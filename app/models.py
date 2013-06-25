# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Estado(models.Model):
	Estado = models.CharField(max_length=30,help_text='Ingrese El estado Civil')
		
	def __unicode__(self):
		return self.Estado
	class Meta:
		verbose_name=u'Estados Civile'

class Flet(models.Model):
	nivel = models.CharField(max_length=30,help_text='Ingrese El nivel')
		
	def __unicode__(self):
		return self.nivel
	class Meta:
		verbose_name=u'Facultad Latinoamericana De Estudios Teologicos'

class Clases_Crecimiento(models.Model):
	nivel = models.CharField(max_length=30,help_text='Ingrese El nivel')
		
	def __unicode__(self):
		return self.nivel
	class Meta:
		verbose_name=u'Clases de Crecimiento'




class Datos(models.Model):
	
	
    Usuario = models.OneToOneField(User)
    Fletn = models.ForeignKey(Flet, help_text='Flet nivel', null=True, blank=True)
    CC = models.ForeignKey(Clases_Crecimiento,help_text='Ingrese la Clase De Crecimiento', null=True, blank=True)   
    FechaNacimiento = models.DateField()
    
    EstadoCivil = models.ForeignKey(Estado,help_text='Ingrese El estado Civil')
    Conyuge = models.CharField(max_length=100,null=True, blank=True)
    

    Trabajo = models.CharField(max_length=40,null=True, blank=True)
    Institucion_Trabajo = models.CharField(max_length=40, null=True, blank=True)
    
    
	
	
	

    Titulo = models.CharField(max_length=40,null=True, blank=True,help_text='Nivel Academico')
    Titulo_CE = models.CharField(max_length=40, null=True, blank=True,help_text='Centro de Estudios')
    TituloTeo = models.CharField(max_length=40,null=True, blank=True,help_text='Nivel Academico')
    TituloTeo_CE = models.CharField(max_length=40, null=True, blank=True,help_text='Centro de Estudios')
    
    Telefono = models.IntegerField(max_length=10, help_text='Numero Convencional', null=True, blank=True)	
    Celular = models.IntegerField(max_length=10, help_text='Numero Celular', null=True, blank=True)

    lat = models.CharField(max_length=30,help_text='Latitud',null=True,blank=True)
    lon_g =	models.CharField(max_length=30,help_text='Longitud',null=True,blank=True)
    Direccion = models.TextField(max_length=200, help_text='Lugar', null=True, blank=True) 

    class Meta:
		verbose_name=u'Datos Principale'

class Calendario(models.Model):
	Autor = models.ForeignKey(User)

	Titulo = models.CharField(max_length=40,help_text='Evento') 
	Lugar = models.CharField(max_length=40,help_text='Evento') 
	Inicio = models.IntegerField(max_length=4,help_text='Hora de Inicio')
	Final = models.IntegerField(max_length=4,help_text='Hora de Finalización')

	 

	FechaU = models.DateField()
	FechaI = models.DateField()
	
	Contenido = models.TextField(max_length=1000,help_text='Contenido')

	class Meta:
		verbose_name=u'Calendario'



