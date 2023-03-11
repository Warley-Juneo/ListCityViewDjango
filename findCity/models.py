from django.db import models

class State(models.Model):
	class Meta:
		verbose_name = u'estado'

	name = models.CharField(max_length=100, verbose_name=u'nome')
	slug = models.CharField(max_length=2, verbose_name=u'sigla')

class City(models.Model):

	state = models.ForeignKey(State, verbose_name=u'estado',on_delete=models.CASCADE)
	name = models.CharField(max_length=100, verbose_name=u'nome da cidade', null=True, blank=True)
