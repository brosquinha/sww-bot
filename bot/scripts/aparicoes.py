# -*- coding: utf-8  -*-
"""
Gets all appearances from a media page (book, movie, comics, etc) and adds
to each one appearance page's Appearance section the media page name

Example: gets all characters, ships, planets, etc, appearances from The
Essential Atlas article. Then, goes to every page of this list and adds
to its Appearance section (if it has one, otherwise it will create this
section) "*''[[The Essential Atlas]]''

The goal with this script is to allow a complete list of appearances
on a reference article to update all articles affected by this one list.
"""
import getopt
import os
import re
import sys
import time
from typing import Tuple, Union

import pywikibot
from pywikibot import pagegenerators

from bot.core.replace import main as replace_bot
from bot.utils import get_user_yes_or_no, swwsite


class AppearanceItem():
	"""
	An Appearance item to be added to its given article
	"""
	def __init__(
			self,
			appearance_item: str,
			article_name: str,
			article_link_format: Tuple[str, str]
	):
		"""
		:param appearance_item: Text of an item of {{App}} whose article will be edited
		:type appearance_item: String)
		:param article_name: Name of the article to be added as appearance
		:type article_name: String)
		:param article_link_format: Format in which the article link must be presented (default: ''[[]]'')
		:type article_link_format: tuple(String, String)
		"""
		self.source_article_name = article_name
		self.source_article_link_format = article_link_format
		regular_link = re.search(
			r'\[\[([^}\]\|]*)\|?([^}\|\]]*)\]\](.*)$|\{\{SUBST\:Legends\|([^}\]\|]*)\|?([^}\|\]]*)\}\}(.*)$|\{\{Legends\|([^}\]\|]*)\|?([^}\|\]]*)\}\}(.*)$',
			appearance_item,
			re.MULTILINE
		)
		if regular_link:
			self.subject_article_name: Union[str, None] = (
				regular_link.group(1) or 
				regular_link.group(4) or regular_link.group(7)
			)
			self.subject_visible_name: Union[str, None] = (
				regular_link.group(2) or 
				regular_link.group(5) or regular_link.group(8)
			)
			self.subject_complement: Union[str, None] = (
				regular_link.group(3) or 
				regular_link.group(6) or regular_link.group(9)
			)
			if self.subject_article_name == None:
				raise Exception('Invalid appearance_item (could not find name): "{}"'.format(appearance_item))
		else:
			raise Exception('Invalid appearance_item: "{}"'.format(appearance_item))

	def format_appearance_link(
			self,
			article_name: str,
			format: Tuple[str, str]=("''[[", "]]''")
	) -> str:
		"""
		Formats article appearance link to article with given format

		:param article_name: Name of the article to be linked
		:type article_name: String
		:param format: Format in which the article link must be presented (default: ''[[]]'')
		:type format: tuple(String, String)
		:return: Link item formatted to be inserted into Appearances section
		:rtype: String
		"""
		return '*{}{}{}'.format(format[0], article_name, format[1])

	def get_article_page(self, site: pywikibot.Site) -> pywikibot.Page:
		"""
		Gets subject's page from wiki

		:param site: A pywikibot.Site object for the wiki
		:type site: pywikibot.Site
		:return: A pywikibot.Page object for the subject article
		:rtype: pywikibot.Page
		"""
		self.subject_article_page = pywikibot.Page(site, self.subject_article_name)
		return self.subject_article_page
	
	def has_link_to_article_already(self) -> bool:
		"""
		Whether subject page already has article in its Appearances section

		:rtype: Boolean
		"""
		return self.subject_article_page.text.find(self.source_article_name) > -1

	def has_link_to_article_original_name_already(
			self, article_original_name: str) -> bool:
		"""
		Whether subject page already has article's original title in its Appearances section

		:rtype: Boolean
		"""
		return self.subject_article_page.text.find(article_original_name) > -1

	def has_appearance_section(self) -> bool:
		"""
		Whether subject page has a Appearances section

		:rtype: Boolean
		"""
		return self.subject_article_page.text.find("Aparições") > -1

	def insert_appearance_item(self) -> None:
		"""
		Inserts an item in subject's Appearances section for the article
		"""
		print("Temos de adicionar esta aparição para {}".format(
			self.subject_article_name))
		subject_text = self.subject_article_page.text
		textoAntes = subject_text.split("Aparições", 1)
		secApar = textoAntes[1].split("\n")[1:]
		textoAntes = textoAntes[0]
		secApar = "\n".join(secApar)
		secAparAdd = secApar.split("\n*", 1)
		aparicao = self.format_appearance_link(
			self.source_article_name, self.source_article_link_format)
		try:
			secAparAdd = secAparAdd[0]+"\n"+aparicao+"\n*"+secAparAdd[1]
		except:
			secAparAdd = secApar.split("*", 1)
			secAparAdd = secAparAdd[0]+"\n"+aparicao+"\n*"+secAparAdd[1]
		novoTexto = textoAntes + "Aparições ==\n" + secAparAdd
		self.subject_article_page.text = novoTexto
		self.subject_article_page.save(
			u"([[User:Thales César|Thales]]) 2.5 Adicionando aparições")

	def insert_appearance_section(self) -> None:
		"""
		Creates Appearance section in subject's page with article as an item
		"""
		artPredefs = self.subject_article_page.templates()
		subject_text = self.subject_article_page.text
		temInterlang = False
		for predef in artPredefs:
			predef = predef.title()
			if (predef=="Predefinição:Interlang"):
				temInterlang = True
				print("Tem Interlang")
				break
		try:
			h2s = subject_text.split("\n==")
			h2s = h2s[1:]
			cabecalhos = []
			print("Cabeçalhos do artigo:")
			for h2 in h2s:
				h2 = h2.split("\n")[0]
				h2 = h2.replace("=", '')
				h2clean = h2.strip()
				cabecalhos.append(h2clean)
				print(" "+h2clean)
				h2WsAntes = h2.split(h2clean)[0]
				h2WsDepois = h2.split(h2clean)[1]
		except:
			print("Não há cabeçalhos...")
		secaoAparicoes = "\n== Aparições ==\n"+self.format_appearance_link(self.source_article_name, self.source_article_link_format)+"\n\n"
		if ("Fontes" in cabecalhos):
			textoPreFontes = subject_text.split("=="+h2WsAntes+"Fontes"+h2WsDepois+"==")
			textoPosFontes = "== Fontes =="+textoPreFontes[1]
			textoPreFontes = textoPreFontes[0] + secaoAparicoes
			novoTexto = textoPreFontes + textoPosFontes
		elif ("Notas e referências" in cabecalhos):
			textoPreFontes = subject_text.split("=="+h2WsAntes+"Notas e referências"+h2WsDepois+"==")
			textoPosFontes = "== Notas e referências =="+textoPreFontes[1]
			textoPreFontes = textoPreFontes[0] + secaoAparicoes
			novoTexto = textoPreFontes + textoPosFontes
		elif (temInterlang):
			textoPreInterlang = subject_text.split("{{Interlang")
			textoPosInterlang = "{{Interlang"+textoPreInterlang[1]
			textoPreInterlang = textoPreInterlang[0] + secaoAparicoes
			novoTexto = textoPreInterlang + textoPosInterlang
		else:
			novoTexto = subject_text + secaoAparicoes
		try:
			novoTexto
			self.subject_article_page.text = novoTexto
			self.subject_article_page.save(
				u"([[User:Thales César|Thales]]) 2.5 Adicionando aparições")
		except NameError:
			print("Nenhuma ação tomada em {}...".format(self.subject_article_name))

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'p:', ["page="])
		for opt, arg in opts:
			if opt in ('-p', '--page'):
				myPage = arg
	except getopt.GetoptError:
		myPage = input("Qual página? ")
	site = swwsite
	try:
		myPage
	except NameError:
		myPage = input("Qual página? ")

	apTrad = pywikibot.Page(site, myPage)
		
	if apTrad.exists():
		format_confirmed = False
		myPageFormat = ("''[[", "]]''")
		while not format_confirmed:
			message = ("Modelo de inserção de aparição: {}{}{} ([y]es/[n]o) ".format(
				myPageFormat[0], myPage, myPageFormat[1]))
			if get_user_yes_or_no(message):
				format_confirmed = True
			else:
				myPageFormat = (
					input("Digite a primeira parte do formato: "),
					input("Digite a segunda parte do formato: ")
				)
		myPageEnglish = None
		if get_user_yes_or_no("É uma obra traduzida? Existe a possbilidade de haver o nome em inglês dela por aí? ([y]es/[n]o) "):
			universo = input("Informe se é uma obra Cânon ou Legends ([L]egends/[C]ânon): ").lower()
			if (universo == "c"):
				universo = "0"
			else:
				universo = "114"
			myPageEnglish = input("Agora, informe o nome da obra em inglês: ")
			replace_bot(myPageEnglish, myPage, "-ns:{}".format(universo), "-start:!")
		conteudo = apTrad.text
		try:
			lista = conteudo.split("{{App")[1]
			lista = lista.split("\n}}")[0]
			links = lista.split("\n*")
			links = links[1:]
		except:
			print("{} não tem {}!".format(myPage, "{{App}}"))
			exit(0)
		for recorte in links:
			try:
				appearance_item = AppearanceItem(recorte, myPage, myPageFormat)
			except Exception as e:
				print(e.args)
				if input("Continuar? ([y]es/[n]o) ").lower() != 'y':
					break
			print(appearance_item.subject_article_name)
			page = appearance_item.get_article_page(site)
			if not page:
				print("Erro ao abrir {}...".format(appearance_item.subject_article_name))
				continue
			if not page.exists():
				print('{} não existe...'.format(appearance_item.subject_article_name))
				continue
			if page.isRedirectPage():
				appearance_item.subject_article_page = page.getRedirectTarget()
				if appearance_item.subject_article_page.isRedirectPage():
					print(
						'{} é um redirecionamento duplo ou coisa pior... corrigir antes de continuar'.format(
							appearance_item.subject_article_name
					))
					continue
				appearance_item.subject_article_name = appearance_item.subject_article_page.title()
			if appearance_item.has_link_to_article_already():
				print("{} já tem essa aparição...".format(appearance_item.subject_article_name))
			else:
				if appearance_item.has_appearance_section():
					appearance_item.insert_appearance_item()
				else:
					message = (
						'{} não tem a seção "Aparições"... criar uma? ([y]es/[n]o)'.format(
							appearance_item.subject_article_name))
					if get_user_yes_or_no(message):
						appearance_item.insert_appearance_section()
					else:
						print("Nenhuma ação tomada em {}".format(
							appearance_item.subject_article_name))
	else:
		print(myPage+" não existe!")
