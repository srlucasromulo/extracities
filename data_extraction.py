import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'extracities.settings'
django.setup()

from database.models import Reg_Ter, Repasse_FNS
import pandas as pd


def extract_from_relatorio():
	df = pd.read_csv(
		'data/RELATORIO_DTB_BRASIL_MUNICIPIO.csv', encoding='iso-8859-1', low_memory=False, sep=';'
	)

	for row in df.iloc:
		registro = Reg_Ter(
			uf=row['UF'],
			nome_UF=row['Nome_UF'],
			regiao_geografica_intermediaria=row['Região Geográfica Intermediária'],
			nome_regiao_geografica_intermediaria=row['Nome Região Geográfica Intermediária'],
			regiao_geografica_imediata=row['Região Geográfica Imediata'],
			nome_regiao_geografica_imediata=row['Nome Região Geográfica Imediata'],
			mesorregiao_geografica=row['Mesorregião Geográfica'],
			nome_mesorregiao=row['Nome_Mesorregião'],
			microrregiao_geografica=row['Microrregião Geográfica'],
			nome_microrregiao=row['Nome_Microrregião'],
			municipio=row['Município'],
			codigo_municipio_completo=row['Código Município Completo'],
			nome_municipio=row['Nome_Município'],
			cod_municipio=row['Código  Município - 6 dígitos'],
		)
		registro.save()
		# print(f'{registro.nome_municipio}')   # verbose


# converte valor str para float
def get_value(value: str):
	return float(value.replace("'", '').replace('.', '').replace(',', '.'))


def extract_from_xls(planilha):
	# colunas necessarias e seus nomes
	select_columns = [1, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
	columns_names = [
		'bloco', 'grupo', 'acao_detalhada', 'competencia_parcela',
		'num_ob', 'data_ob', 'banco_ob', 'agencia_ob', 'conta_ob',
		'valor_total', 'desconto', 'valor_liquido', 'observacao',
		'processo',  'tipo_repasse', 'num_proposta'
	]

	df = pd.read_excel(planilha)

	# extrai o código do municipio
	cod_municipio = df['Unnamed: 7'].iloc[2]

	# seleciona apenas as colunas necessarias e renomeia
	df = df.loc[:, [f'Unnamed: {i}' for i in select_columns]]
	df.columns = columns_names

	# remove cabecalho
	df = df.iloc[7:]

	# remove linhas nulas
	df = df.loc[df.bloco.notna()]

	for row in df.iloc:
		registro = Repasse_FNS(
			bloco=row.bloco,
			grupo=row.grupo,
			acao_detalhada=row.acao_detalhada,
			competencia_parcela=row.competencia_parcela,
			num_ob=row.num_ob,
			data_ob=row.data_ob,
			banco_ob=row.banco_ob,
			agencia_ob=row.agencia_ob,
			conta_ob=row.conta_ob,
			valor_total=get_value(row.valor_total),
			desconto=get_value(row.desconto),
			valor_liquido=get_value(row.valor_liquido),
			observacao=row.observacao,
			processo=row.processo,
			tipo_repasse=row.tipo_repasse,
			num_proposta=row.num_proposta,
			cod_municipio=Reg_Ter.objects.get(cod_municipio=cod_municipio)
		)
		registro.save()
		# print(f'{registro.cod_municipio}, {registro.id}')   # verbose


def extract_from_planilhas():
	# log de planilhas que falharam
	open('failed_planilha.log', 'w').close()

	# get planilhas
	path = './data/'
	planilhas = os.popen(f'ls {path} | grep PlanilhaDetalhada').readlines()

	for planilha in planilhas:
		try:
			extract_from_xls(path + planilha.strip())
		except:
			with open('failed_planilha.log', 'a') as file:
				file.write(planilha.strip() + '\n')
				file.close()
