# -*- coding: utf-8  -*-
"""
Updates Template:TraduçãoSWW with contents from Apêndice de Tradução
"""
import sys, getopt
import pywikibot
from pywikibot import pagegenerators

from bot.utils import swwsite as site

def main():
	apTrad = pywikibot.Page(site, u"Star Wars Wiki:Apêndice de Tradução")

	if apTrad:
		nome = apTrad.title()
		print("\r")
		print(nome)
		conteudo = apTrad.text
		lista = conteudo.split("===Listagem===")
		textoAntes = lista[0] + "===Listagem==="
		lista = lista[1].split("{{#if:{{{refs|}}}|{{notes}}{{reflist}}|}}")
		textoDepois = "{{#if:{{{refs|}}}|{{notes}}{{reflist}}|}}" + lista[1]
		lista = lista[0]
		termos = lista.split("\n*")[1:]
		textoFinal = "{{#switch: {{lc:{{{1}}}}}\n"
		for termo in termos:
			termo = termo.replace("{{L|", '')
			termo = termo.replace("{{l|", '')
			termo = termo.split("\n")[0].split("<ref")[0].split("|")[0]  #Desculpe se isso é meio porco...
			termo = termo.replace("'", '') #Deve ter alguma forma de fazer isso melhor...
			termo = termo.replace("*", '')
			termo = termo.replace("[", '')
			termo = termo.replace("]", '')
			termo = termo.replace("}", '')
			termo = termo.replace("Legends:", '')
			if (termo.count("=") != 1):
				print("Erro em '"+termo+"': número incorreto de sinais de igual! Pulando linha...")
				continue
			termoAux = termo.split("=")
			termoArgm = termoAux[0].lower()
			termo = termoArgm + "=" + termoAux[1]
			if (termo.find("(") > -1):
				termoAux = termo.split("(")
				termo = termoAux[0]
				termoAux = termoAux[1:]
				for txtAux in termoAux:
					termo += txtAux.split(")")[1]
			termo = "|" + termo
			textoFinal += termo + "\n"
		predef = pywikibot.Page(site, u"Predefinição:TraduçãoSWW")
		conteudoPredef = predef.text
		conteudoPredef = u''.join(conteudoPredef).encode('utf-8')
		conteudoPredef = "|{{{1|}}} " + conteudoPredef.split("|{{{1|}}} ")[1]
		textoFinal += conteudoPredef
		pywikibot.showDiff(predef.text, textoFinal.decode('utf-8'))
		predef.text = textoFinal
		predef.save(u'([[User:Thales César|Thales]]) 2.3 Expansão - Atualizando com conteúdo do Apêndice de Tradução')
		
		idTrad = apTrad.latestRevision()
		print(idTrad)
		salvarArq = open("traducaoSWW.txt", "w")
		salvarArq.write(str(idTrad))
		salvarArq.close()
