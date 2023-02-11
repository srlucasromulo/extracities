from django.db import models


class Reg_Ter(models.Model):
	uf = models.IntegerField()
	nome_UF = models.CharField(max_length=256)
	regiao_geografica_intermediaria = models.IntegerField()
	nome_regiao_geografica_intermediaria = models.CharField(max_length=256)
	regiao_geografica_imediata = models.IntegerField()
	nome_regiao_geografica_imediata = models.CharField(max_length=256)
	mesorregiao_geografica = models.IntegerField()
	nome_mesorregiao = models.CharField(max_length=256)
	microrregiao_geografica = models.IntegerField()
	nome_microrregiao = models.CharField(max_length=256)
	municipio = models.IntegerField()
	codigo_municipio_completo = models.CharField(max_length=7)
	nome_municipio = models.CharField(max_length=256)
	# PK
	cod_municipio = models.CharField(max_length=6, primary_key=True)

	def __str__(self):
		return self.nome_municipio


class Repasse_FNS(models.Model):
	bloco = models.CharField(max_length=256)
	grupo = models.CharField(max_length=256)
	acao_detalhada = models.CharField(max_length=256)
	competencia_parcela = models.CharField(max_length=256)
	num_ob = models.CharField(max_length=256)
	data_ob = models.CharField(max_length=10)
	banco_ob = models.CharField(max_length=3)   # id do banco?
	agencia_ob = models.CharField(max_length=256)
	conta_ob = models.CharField(max_length=256)
	valor_total = models.FloatField()
	desconto = models.FloatField()
	valor_liquido = models.FloatField()
	observacao = models.CharField(max_length=256)
	processo = models.CharField(max_length=256)
	tipo_repasse = models.CharField(max_length=256)
	num_proposta = models.CharField(max_length=256)
	# PK/FK
	id = models.AutoField(primary_key=True)
	cod_municipio = models.ForeignKey(Reg_Ter, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.id}, {self.cod_municipio}'
