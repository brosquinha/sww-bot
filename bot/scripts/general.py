# -*- coding: utf-8  -*-
"""
This script checks for several general activities before running fixing routines.

This script checks and may run the following tasks:
* Wrong canon links in Legends articles
* Double redirects
* Sandbox page
* TraduçãoSWW
* Canon timeline translation
* Unused files
"""
import os
import sys
import time

import pywikibot
import urllib3
from pywikibot import pagegenerators

from bot.core import clean_sandbox, redirect, unusedfiles
from bot.scripts import linha_do_tempo
from bot.scripts import links_canon as canon
from bot.scripts import traducaoSWW
from bot.utils import get_user_yes_or_no, swwsite as site


def main():
	print("Checando todas as tarefas de manutenção do bot:")
	print("	Links errados")
	print("	Redirecionamentos duplos")
	print("	Página de testes")
	print("	TraducaoSWW")
	print("	Linha do tempo")
	print("	Imagens não utilizadas")

	### Links errados ###
	category = pywikibot.Category(site,'Category:Artigos com links errados')
	generator = pagegenerators.CategorizedPageGenerator(category, False)
	try:
		next(generator)
		if get_user_yes_or_no("Há artigos Cânon para se corrigir links. ([y]es/[n]o)"):
			canon.main()
		else:
			print("OK, deixa pra lá...")
	except StopIteration:
		print("Não há artigos Cânon para se corrigir links...")

	### Redirecionamentos duplos ###
	numPags = 0
	pages = iter(site.double_redirects())
	try:
		next(pages)
		if get_user_yes_or_no("Há redirecionamentos duplos a serem corrigidos. ([y]es/[n]o)"):
			redirect.main('double', '-always')
		else:
			print("OK, deixa pra lá...")
	except StopIteration:
		print("Não há redirecionamentos duplos...")
		
	### Página de testes ###
	test_page = pywikibot.Page(site, u"Star Wars Wiki:Testes")
	if test_page:
		test_page_txt = test_page.text
		actual_test_content = test_page_txt.split("----")[1]
		actual_test_content = actual_test_content.replace("\r", '')
		actual_test_content = actual_test_content.replace("\n", '')
		if (actual_test_content!=''):
			if get_user_yes_or_no("É necessário limpar a página de testes. ([y]es/[n]o)"):
				clean_sandbox.main('-delay:5')
			else:
				print("OK, deixa pra lá...")
		else:
			print("Página de testes OK...")
	else:
		print("Não foi possível obter a página de testes...")
		
	### TraducaoSWW ###
	try:
		temp_file = open("traducaoSWW.txt")
		ultimoID = temp_file.read()
	except FileNotFoundError:
		ultimoID = False
	finally:
		temp_file.close()
	apTrad = pywikibot.Page(site,u"Star Wars Wiki:Apêndice de Tradução")
	idTrad = apTrad.latestRevision()
	if str(idTrad) == ultimoID:
		print("{{TraduçãoSWW}} atualizada...")
	else:
		if get_user_yes_or_no("É necessário atualizar {{TraduçãoSWW}}. ([y]es/[n]o)"):
			traducaoSWW.main()
		else:
			print("OK, deixa pra lá...")
			
	### Linha do tempo ###
	url = "http://starwars.wikia.com/wiki/Timeline_of_canon_media?action=raw"
	request = urllib3.PoolManager()
	try:
		response = request.request("GET", url, timeout=30)
		wookiee_timeline = response.data.decode('utf-8')
		try:
			temp_file = open("last_content_of_canon_media_timeline.txt")
			local_page = temp_file.read()
		except FileNotFoundError:
			local_page = False
		finally:
			temp_file.close()
		if local_page == wookiee_timeline:
			print("Linha do tempo canônica atualizada...")
		else:
			if get_user_yes_or_no("É necessário atualizar a linha do tempo canônica. ([y]es/[n]o)"):
				linha_do_tempo.main()
			else:
				print("OK, deixa pra lá...")
	except:
		print("Não foi possível obter linha do tempo da Wookieepedia.")

	### Imagens não utilizadas ###
	numPags = 0
	pages = site.unusedfiles()
	my_user = site.getuserinfo()
	my_username = my_user['name']
	my_user_groups = my_user['groups']
	temPags = False
	outputStrLen = 0
	check_images = True
	pagesList = list(pages)
	if (len(pagesList) > 50):
		check_images = get_user_yes_or_no(
			"Verificar por imagens a serem deletadas pode demorar.\nVerificar mesmo assim? ([y]es/[n]o) ")
	if (check_images):
		for page in pages:
			categorias = list(page.categories())
			outputStr = "Vendo "+page.title()
			sys.stdout.write("\r")
			sys.stdout.flush()
			sys.stdout.write(" "*outputStrLen)
			sys.stdout.flush()
			sys.stdout.write("\r")
			sys.stdout.flush()
			sys.stdout.write(outputStr)
			sys.stdout.flush()
			outputStrLen = len(outputStr)
			if (page.exists() and not categorias):
				print("\nDeletar!")
				temPags = True
				break
		if (temPags==True):
			if (u'sysop' in my_user_groups):
				message = "Há imagens não utilizadas a serem deletadas. ([y]es/[n]o)"
				is_bot_admin = True
			else:
				message = "Há imagens não utilizadas a serem marcadas para deleção. ([y]es/[n]o)"
				is_bot_admin = False
			if get_user_yes_or_no(message):
				unusedfiles.main('-always')
				if is_bot_admin == False:
					print("\nDepois, troque o usuário para Thales César e rode deletar.sh")
					time.sleep(3)
			else:
				print("OK, deixa pra lá...")
		else:
			print("\nNão há imagens não utilizadas...")
	else:
		print("Imagens não utilizadas não foram verificadas...")

	### Avisos finais ###
	print("\nTarefas automáticas de manutenção finalizadas. Há, ainda, outras tarefas de manutenção manuais a serem executadas periodicamente.")
	pywikibot.output("\03{lightblue}Outras tarefas: \03{default}")
	print("\t remover_predefs.py")
	print("\t eras_canon.py")
	print("\t replace.py -fix:obras -start:! -ns:112")
	print("\t canon.sh e canon_aux.sh")
