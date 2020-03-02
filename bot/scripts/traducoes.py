# -*- coding: utf-8  -*-
"""
Updates Apêndice de Tradução based on community-maintained spreadsheet with all translations
"""
import csv

import pywikibot
import urllib3
from pywikibot import pagegenerators

from bot.utils import get_user_yes_or_no
from bot.utils import swwsite as site

url = "https://docs.google.com/spreadsheets/d/1y533tW-af2g__rTyeKkuewIrLqjiKVK6CFKMv89s46A/gviz/tq?tqx=out:csv&sheet=Termos"
article_names = {
	"Provação": "Provação (romance)",
	"Kenobi": "Kenobi (romance)"
}

def upper_first_letter(txt):
	return txt[0].upper() + txt[1:]

def format_article_link(txt):
	"""
	Outputs MediaWiki link to out-of-universe article

	:param txt: Out-of-universe article common name
	:type txt: String
	:return: Formatted MediaWiki link
	:rtype: String
	"""
	if txt in article_names:
		return "[[{}|{}]]".format(article_names[txt], txt)
	return "[[{}]]".format(txt)

def main():
	print("Obtendo planilha Termos...")
	request = urllib3.PoolManager()
	try:
		response = request.request("GET", url, timeout=10)
		excelAT = response.data.decode('utf-8')
	except:
		print("Não foi possível obter planilha")
		return
		
	excelAT = excelAT.split("\n")[1:]
	excelAT = csv.reader(excelAT)
	att_page = pywikibot.Page(site, u"Star Wars Wiki:Apêndice de Tradução")
	att_text = att_page.text
	att_list = {}
	att_list_original = att_text.split("\n*")[1:]
	for l in att_list_original:
		if (l.count("=") < 1):
			continue
		l_traducao = l.split("=")[1]
		if (l_traducao.find("\n") > -1):
			l_traducao = l_traducao.split("\n")[0]
		elif (l.count("=") > 1):
			for m in l.split("=")[2:]:
				if (m.find("\n") > -1):
					l_traducao = l_traducao + "=" + m.split("\n")[0]
					break
				else:
					l_traducao = l_traducao + "=" + m
		l_original = l.split("=")[0].replace("''", '').strip()
		if (l_original[0] == "*"):
			l_original = l_original[1:]
		att_list[upper_first_letter(l_original)] = l_traducao.strip()

	for row in excelAT:
		word_original = row[0].strip()
		word_translated = row[1].strip()
		translation_source = row[2].strip()
		translator = row[3].strip()
		alternatives_trans = row[4].strip()
		notes = row[5].strip()
		if (word_original == '' or word_translated == ''):
			continue
		ref = ''
		if (translation_source != ''):
			if (translation_source == 'Convenção'):
				ref = '<ref name="convenção">{}'.format(translation_source)
			elif (translation_source[0:4] == 'TCW:'):
				ref = '<ref name="{name}">{{{{TCW|{source}}}}}'.format(
					name=translation_source[4:].strip(),
					source=translation_source[4:].strip()
				)
			else:
				ref = '<ref name="{name}">\'\'{source_link}\'\''.format(
					name=translation_source.replace(":", ""),
					source_link=format_article_link(translation_source)
				)
			if (translator == ''):
				ref = "{}</ref>".format(ref)
			else:
				ref = '{ref}, traduzido por {translator}</ref>'.format(
					ref=ref,
					translator=translator
				)
		if (notes != ''):
			ref = '{ref}<ref group="nota">{notes}</ref>'.format(
				ref=ref,
				notes=notes
			)
				
		att_list[upper_first_letter(word_original)] = word_translated + ref

	final_text = att_text.split("\n*")[0]
	last_first_letter = 'a'
	for key in sorted(att_list):
		word_original = key
		word_translated = att_list[key]
		first_letter = word_original[0]
		if (ord(first_letter) >= ord('A') and first_letter != last_first_letter):
			final_text = final_text + "\n<noinclude>===="+first_letter+"====</noinclude>\n<includeonly>\n:'''"+first_letter+"''' </includeonly>"
			last_first_letter = first_letter
		final_text = final_text + "\n*" + word_original + " = " + word_translated

	final_text = final_text + "\n{{#if:{{{refs|}}}|{{notes}}{{reflist}}|}}" + att_text.split("{{#if:{{{refs|}}}|{{notes}}{{reflist}}|}}")[1]
	pywikibot.showDiff(att_page.text, final_text)
	if get_user_yes_or_no("Salvar? ([y]es/[n]o) "):
		att_page.text = final_text
		att_page.save(u'([[User:Thales César|Thales]]) 2.3 Expansão - Atualizando com conteúdo da planilha')
