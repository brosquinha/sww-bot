# -*- coding: utf-8  -*-
"""
Replaces canon links for Legends links on pages marked as containg incorrect links.

On Star Wars Wiki, in-universe articles are divided into two universes: Canon and Legends.
We organize them into different namespaces, so that there can be no conflict between them.
As such, it is imperative that canon articles link to other canon articles, and Legends link
to other Legends pages. Because Legends linking requires the prefix "Legends:" on every Legends
link, it is quite common for new users to forgo the namespace and make a lot of canon links on
Legends articles. This scripts aims to help fix those links.
"""
import json
import sys, getopt
from json.decoder import JSONDecodeError

import pywikibot
from pywikibot import pagegenerators

from bot.utils import swwsite as site


def main():
	try:
		with open("links_canon.json") as f:
			known_links = json.loads(f.read())
	except (FileNotFoundError, OSError, JSONDecodeError):
		known_links = {'legends': [], 'canon': []}

	category = pywikibot.Category(site,'Category:Artigos com links errados')
	generator = pagegenerators.CategorizedPageGenerator(category, True)

	for links_legends, links_not_legends in replace_links(page_generator=generator, known_links=known_links):
		with open("links_canon.json", "w+") as f:
			f.write(json.dumps({'legends': links_legends, 'canon': links_not_legends}))

def replace_links(page_generator, known_links):
	already_confirmed = known_links.get('legends', [])
	already_denied = known_links.get('canon', [])
	all_next = False

	for page in page_generator:
		nome = page.title()
		print(nome)
		if (nome == "Predefinição:Links errados/preload"):
			continue
		conteudo = page.text
		links = conteudo.split("[[")
		novoTexto = links[0]
		links = links[1:]
		skip_these = ["File:", "Ficheiro:", "Imagem:", "Image:", "Category:", "Categoria:", "Legends:"]
		for recortes in links:
			recortes = recortes.split("]]")
			link = recortes[0]
			try: 
				recorteFinal1 = recortes[1]
				recorteFinal = ']]'.join(recortes[1:])
			except:
				novoTexto += "[[" + link
				continue
			if (link.find("|") > -1):
				actual_article_name = link.split("|")[0]
				link_name = link.split("|")[1]
			else:
				actual_article_name = link
				link_name = False
			
			if any(ext in actual_article_name for ext in skip_these):
				print("Pulando '" + actual_article_name + "'...")
				novoTexto += "[[" + link + "]]" + recorteFinal
			elif (actual_article_name in already_denied):
				print("Pulando '" + actual_article_name + "'...")
				novoTexto += "[[" + link + "]]" + recorteFinal
			elif (actual_article_name in already_confirmed):
				print("Substituindo por Legends '" + actual_article_name + "' (yes)")
				if (link_name):
					novoTexto += "[[Legends:" + actual_article_name + "|" + link_name + "]]" + recorteFinal
				else:
					novoTexto += "[[Legends:" + actual_article_name + "|" + actual_article_name + "]]" + recorteFinal
			else:
				print("Substituir por Legends: '" + actual_article_name + "' ([y]es/[n]o/[e]dit (Legends)/[c]orrect (Cânon)/[a]ll)")
				if all_next:
					averiguar = "y"
				else:
					averiguar = input().lower()
				if (averiguar == "y" or averiguar == "a"):
					if (link_name):
						novoTexto += "[[Legends:" + actual_article_name + "|" + link_name + "]]" + recorteFinal
					else:
						novoTexto += "[[Legends:" + actual_article_name + "|" + actual_article_name + "]]" + recorteFinal
					already_confirmed.append(actual_article_name)
					if (averiguar == "a"):
						all_next = True
				elif (averiguar == "e"):
					if (link_name):
						print('Tem "máscara"!')
					novoLink = input("Novo link Legends: ")
					if (link_name):
						novoTexto += "[[Legends:" + novoLink + "|" + link_name + "]]" + recorteFinal
					else:
						novoTexto += "[[Legends:" + novoLink + "|" + novoLink + "]]" + recorteFinal
					if novoLink not in already_confirmed:
						already_confirmed.append(novoLink)
				elif (averiguar == "c"):
					if (link_name):
						print('Tem "máscara"!')
					novoLink = input("Novo link normal: ")
					if (link_name):
						novoTexto += "[[" + novoLink + "|" + link_name + "]]" + recorteFinal
					else:
						novoTexto += "[[" + novoLink + "]]" + recorteFinal
					if novoLink not in already_denied:
						already_denied.append(novoLink)
				else:
					novoTexto += "[[" + link + "]]" + recorteFinal
					already_denied.append(actual_article_name)
			yield already_confirmed, already_denied

		novoTexto = novoTexto.replace("{{Links errados}}", '')
		novoTexto = novoTexto.replace("{{links errados}}", '')
		page.text = novoTexto
		page.save(u'([[User:Thales César|Thales]]) 3.4 Link Cânon para Legends')
