# -*- coding: utf-8 -*-
"""
This scripts removes Emuso template from pages that have not been edited by
Emuso's user for more than 3 months
"""
import datetime
import getopt
import os
import sys
import time

import pywikibot
from pywikibot import pagegenerators

site = pywikibot.Site(fam="starwarsfandom", code='pt', user='BB-08')

def main():
	cat = pywikibot.Category(site, "Categoria:Páginas sendo editadas")
	gen = pagegenerators.CategorizedPageGenerator(cat, recurse=False)
	dataLimite = 60*60*24*30*3
	for page in gen:
		nome = page.title()
		if (nome == "Predefinição:Emuso/preload"):
			continue
		pywikibot.output(u">>> \03{lightpurple}%s\03{default} <<<" % page.title())
		historico = page.revisions(reverse=True, content=True)
		jaAchei = False
		retirando = False
		for hist in historico:
			dataAki = str(hist.timestamp).split("T")[0]
			dataUTC = time.mktime(datetime.datetime.strptime(dataAki, "%Y-%m-%d").timetuple())
			dataAgora = time.time()
			dataDif = int(dataAgora) - int(dataUTC)
			textoAki = hist.text
			textoAkiL = textoAki.lower()
			if (textoAkiL.find("{{emuso") > -1 and jaAchei==False):
				print("Achei!")
				jaAchei = True
				userAki = hist.user
				print(" ID: "+str(hist.revid)+"\n User: "+userAki+"\n Qndo: "+str(hist.timestamp))
				userEmuso = hist.user
				if (dataDif > dataLimite):
					retirando = True
				else:
					pywikibot.output("\03{lightgreen}Mantendo esta {{Emuso}}...\03{default}")
					retirando = False
					break
			elif (jaAchei==True and hist.user==userEmuso):
				if (dataDif > dataLimite):
					retirando = True
				else:
					pywikibot.output("\03{lightgreen}Mantendo esta {{Emuso}}...\03{default}")
					retirando = False
					break
			else:
				print("Ainda não... ")
		if (retirando==True):
			pywikibot.output("\03{red}Partiu retirar esta {{Emuso}}\03{default}!")
			conteudo = page.text
			if (conteudo.find("{{emuso|") > -1):
				conteudo = conteudo.replace("{{emuso", "{{Emuso")
			auxiliarEmuso = conteudo.split("{{Emuso")
			novoTexto = auxiliarEmuso[0]
			auxiliar = auxiliarEmuso[1].split("}}")
			novoTexto += "}}".join(auxiliar[1:])
			page.text = novoTexto
			page.save(u'([[User:Thales César|Thales]]) 5.3 Emuso removida')
		time.sleep(3)
