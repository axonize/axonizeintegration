# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


opciones = (
    ('Temperatura/Humedad', 'Temperatura/Humedad'),
    ('Temperatura', 'Temperatura'),	
    ('Movimiento', 'Movimiento'),
    ('Detector Voltaje', 'Detector Voltaje'),
    ('Medidor Voltaje', 'Medidor Voltaje'),
	('Corriente Trifasica', 'Corriente Trifasica'),
	('Detector Puerta', 'Detector Puerta'),
	('Ultrasonico', 'Ultrasonico'),
	('Gateway', 'Gateway'),

)

# Create your models here.
class Ejemplo(models.Model):
	datos= models.TextField(max_length=2000)

class SensoresClaro(models.Model):
	Monnit_ID=models.CharField(max_length=20)
	#Device_ID=models.CharField(max_length=20)
	Autorizacion=models.CharField(max_length=300)
	Tipo = models.CharField(max_length=50, choices=opciones)

	def __unicode__(self):
		return str(self.Monnit_ID)
