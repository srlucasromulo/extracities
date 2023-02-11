import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'extracities.settings'
django.setup()

from database.models import Reg_Ter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep
from multiprocessing import Pool

from unidecode import unidecode


URL = 'https://consultafns.saude.gov.br/#/detalhada'


def click_btn(button):
	while True:
		try:
			button.click()
			break
		except:
			pass


def task(municipio):
	# cria o driver
	driver = webdriver.Chrome()
	driver.implicitly_wait(3)

	# acessa o site do FNS
	driver.get(URL)

	# espera o site carregar
	sleep(3)

	# seleciona 2023 no dropdown de ano
	selector = Select(driver.find_element(By.ID, 'ano'))
	selector.select_by_visible_text('2023')

	# seleciona MG no dropdown de estado
	selector = Select(driver.find_element(By.ID, 'estado'))
	selector.select_by_visible_text('MINAS GERAIS')

	# seleciona o municipio no dropdown
	selector = Select(driver.find_element(By.ID, 'municipio'))
	selector.select_by_visible_text(municipio)

	# clica em consultar
	consultar_btn = driver.find_element(By.CLASS_NAME, 'app-icone-buscar')
	click_btn(consultar_btn)

	# quantidade de reports do municipio
	reports_len = len(driver.find_elements(By.CLASS_NAME, 'app-icone-ver'))

	# abre cada report e realiza o download
	for i in range(reports_len):
		# seleciona o report atual
		report_btns = driver.find_elements(By.CLASS_NAME, 'app-icone-ver')
		click_btn(report_btns[i])

		# clica no botao de download da planilha
		# espera o loading (por causa do loop na funcao click_btn)
		element = driver.find_element(By.CLASS_NAME, 'app-icone-arquivo-excel')
		click_btn(element)

		# clica no botao de voltar para ir para o proximo report
		back_btn = driver.find_element(By.CLASS_NAME, 'app-icone-seta-unica-esquerda')
		click_btn(back_btn)

	# espera alguns segundos antes de fechar (para n parar nenhum download)
	sleep(3)


# executa task
# se algum levantar excessao, vai para um log dos municipios que falharam
def exec_task(municipio):
	try:
		task(municipio)
	except:
		with open('failed_municipio.log', 'a') as file:
			file.write(f'{municipio}\n')
			file.close()


def get_municipios():
	# busca as instancias que tem UF = MG
	municipios = Reg_Ter.objects.filter(nome_UF='Minas Gerais')

	# retorna uma lista com o nome processado (maiusculo e sem acento)
	return [
		unidecode(municipio.nome_municipio).upper()
		for municipio in municipios
	]


# funcao main
def get_planilhas():
	# log de municipios que falharam
	open('failed_municipio.log', 'w').close()

	# get nome dos municipios de MG
	municipios = get_municipios()
	municipios = ['NEPOMUCENO']

	with Pool() as pool:
		pool.map(exec_task, iter(municipios))
