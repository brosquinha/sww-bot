# -*- coding: utf-8  -*-
"""
Translates Wookieepedia's Timeline of canon media using local dictionary of translations

This script requires a local file called user-fixes.py containg all local media translations.
"""
import re
import urllib3

import pywikibot
from pywikibot import fixes, pagegenerators

from bot.utils import swwsite as site

def main():
	fixes._load_file("bot/user-fixes.py")
	url = "http://starwars.wikia.com/wiki/Timeline_of_canon_media?action=raw"
	print("Obtendo página em inglês...")
	request = urllib3.PoolManager()
	try:
		response = request.request("GET", url, timeout=10)
		paginaWookiee = response.data.decode('utf-8')
	except:
		print("Não foi possível obter página da Wookieepedia")
		exit(0)


	conteudo = paginaWookiee.split("\n{|")[2:]
	conteudo = "\n{|".join(conteudo)
	novoTexto = """{{Eras|canon|legends|real|link=Linha do tempo de mídia Legends}}
{{Vocepode|linha do tempo de mídia canônica|[[Linha do tempo de mídia Legends|linha do tempo de mídia ''Legends'']]}}
{{Evento futuro}}
Essa é uma linha do tempo para '''todas as mídias [[Cânon|canônicas]] de ''[[Star Wars]]''''' lançadas, incluindo filmes, livros, quadrinhos, curtas, material promocional, séries de TV e jogos.

{|{{Prettytable}} class="timeline-toggles" width="100%"
| style="background-color: #92CDDC; text-align: center; width: 20%;" class="film" | Filmes (F)<br />[[#js|(clique para esconder)]]
| style="background-color: #8DB3E2; text-align: center; width: 20%;" class="novel" | Romances (R)<br />[[#js|(clique para esconder)]]
| style="background-color: #CCC1D9; text-align: center; width: 20%;" class="comic" | Quadrinhos (Q)<br />[[#js|(clique para esconder)]]
| style="background-color: #C3D69B; text-align: center;" class="videogame" | Jogos (J)<br />[[#js|(clique para esconder)]]
| style="background-color: #D7E3BC; text-align: center;" class="promotional" | Material promocional (P)<br />[[#js|(clique para esconder)]]
|-
| style="background-color: #B7DDE8; text-align: center;" class="tv" | Televisão (TV)<br />[[#js|(clique para esconder)]]
| style="background-color: #C6D9F0; text-align: center;" class="short" | Curtas (SS)<br />[[#js|(clique para esconder)]]
| style="background-color: #FFFFFF; text-align: center; width: 20%;" class="young" | Livros infantis (LI)<br />[[#js|(clique para esconder)]]
| style="background-color: #FAC08F; text-align: center; width: 20%;" class="junior" | Romances infanto-juvenis (RIJ)<br />[[#js|(clique para esconder)]]
| style="background-color: #D99694; text-align: center;" class="unpublished" | Ainda não lançado<br />[[#js|(clique para esconder)]]
|}

{|"""
	fimTexto = """|}

==Notas e referências==
{{Scroll box|content=
{{Reflist|2}}
}}
*''Página traduzida automaticamente da [[:w:c:starwars:Timeline of canon media|Wookieepedia]], mantida pelo [[Star Wars Wiki:Robôs|bot]] [[Utilizador:BB-08|BB-08]]. Por favor, evite editar essa página, já que o bot a substitui pela tradução mais recente da versão em inglês. Caso identifique algum bug ou carência de tradução, deixe uma mensagem em [[Utilizador Discussão:BB-08|sua página de discussão]].''

{{Interlang
|en=Timeline of canon media
|ru=Хронология каноничных материалов
}}

[[Categoria:Listas do mundo real]]
[[Categoria:Linhas do tempo de mídias]]"""
	conteudo = conteudo.split("|}\n")[:2]
	conteudo = "|}\n".join(conteudo)

	pagina = pywikibot.Page(site,u"Linha do tempo de mídia canônica")
	paginaConteudo = pagina.text
	refs = paginaConteudo.split("<ref name=")[1:]
	refsTraduzidas = {}
	for ref in refs:
		if (ref.find("</ref>") == -1):
			continue
		ref = ref.split("</ref>")[0]
		refName = ref.split(">")[0]
		refsTraduzidas[refName] = ref

	print("Substituindo anos...")
	conteudo = conteudo.replace("BBY/Canon", "BBY")
	conteudo = conteudo.replace("ABY/Canon", "ABY")
	conteudo = re.sub(r'\[\[([0-9])([0-9]*) ([BA])BY\|\1\2 \3BY\]\]', r'[[\1\2 \3BY]]', conteudo)
	conteudo = re.sub(r'\[\[([0-9])([0-9]*) ABY\]\]', r'[[\1\2 DBY]]', conteudo)
	conteudo = re.sub(r'\[\[([0-9])([0-9]*) ABY\|', r'[[\1\2 DBY|', conteudo)
	conteudo = re.sub(r'\[\[([0-9])([0-9]*) BBY\]\]', r'[[\1\2 ABY]]', conteudo)
	conteudo = re.sub(r'\[\[([0-9])([0-9]*) BBY\|', r'[[\1\2 ABY|', conteudo)
	conteudo = re.sub(r'Season ([1-6])', r'Temporada \1', conteudo)
	conteudo = re.sub(r'Episode ([0-9])([0-9]|)', r'Episódio \1\2', conteudo)

	print("Substituindo rótulos...")
	conteudo = conteudo.replace("Unknown placement", "Localização desconhecida")
	conteudo = conteudo.replace("| Year |", "| Ano |")
	conteudo = conteudo.replace("| Title |", "| Título |")
	conteudo = conteudo.replace("| Writer(s) |", "| Autor(es) |")
	conteudo = conteudo.replace("| Released\n", "| Lançado em\n")
	conteudo = conteudo.replace("| N |", "| R |")
	conteudo = conteudo.replace("| C |", "| Q |")
	conteudo = conteudo.replace("| VG |", "| J |")
	conteudo = conteudo.replace("| YR |", "| LI |")
	conteudo = conteudo.replace("| JR |", "| RIJ |")
	conteudo = conteudo.replace("| Title |", "| Título |")
	conteudo = re.sub(r'\|\| ([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])', r'|| \3/\2/\1', conteudo)

	print("Substituindo termos gerais...")
	conteudo = conteudo.replace("Young readers adaptation of", "Adaptação infantil de")
	conteudo = conteudo.replace("Young adult novelization of", "Romantização de jovens adultos de")
	conteudo = conteudo.replace("Game adaptation of", "Game adaptation of")
	conteudo = conteudo.replace("Graphic novelization of", "Romantização gráfica de")
	conteudo = conteudo.replace("Junior novelization of", "Romantização infanto-juvenil de")
	conteudo = conteudo.replace("Game adaptation of", "Adaptação em jogo de")
	conteudo = conteudo.replace("Video game adaptation of", "Adaptação em jogo de")
	conteudo = conteudo.replace("Comic adaptation of", "Adaptação em quadrinhos de")
	conteudo = conteudo.replace("Webcomic adaptation of", "Adaptação em quadrinhos web de")
	conteudo = conteudo.replace("Novelization of", "Romantização de")
	conteudo = conteudo.replace("Adaptation of", "Adaptação de")
	conteudo = conteudo.replace("first act of", "primeiro ato de")
	conteudo = conteudo.replace("second act of", "segundo ato de")
	conteudo = conteudo.replace("third act of", "terceiro ato de")
	conteudo = conteudo.replace("Prologue is set immediately before", "Prólogo acontece imediatamente antes de")
	conteudo = conteudo.replace("Prologue is set during", "Prólogo acontece durante")
	conteudo = conteudo.replace("Prologue is set immediately after", "Prólogo acontece imediatamente depois de")
	conteudo = re.sub('Prologue occurs ([1-9])([0-9]|) years prior', r'Prólogo acontece \1\2 anos antes', conteudo)
	conteudo = conteudo.replace("Epilogue is set immediately before", "Epílogo acontece imediatamente antes de")
	conteudo = conteudo.replace("Epilogue is set immediately after", "Epílogo acontece imediatamente depois de")
	conteudo = conteudo.replace("Prologue and epilogue occur briefly before the events of", "Prólogo e epílogo acontecem brevemente antes dos eventos de")
	conteudo = conteudo.replace("Prelude occurs concurrently to", "Prelúdio ocorre junto com")
	conteudo = conteudo.replace("Prelude occurs at the end of", "Prelúdio ocorre no fim de")
	conteudo = conteudo.replace("Prologue and epilogue occur three decades prior", "Prólogo e epílogo acontecem três décadas antes")
	conteudo = conteudo.replace("Occurs before and concurrently to", "Ocorre antes e junto com")
	conteudo = conteudo.replace("Occurs before, concurrently to, and after", "Ocorre antes, junto com e depois de")
	conteudo = conteudo.replace("Occurs before and after", "Ocorre antes e depois de")
	conteudo = conteudo.replace("Occurs concurrently to and immediately after", "Ocorre junto com e imediatamente depois de")
	conteudo = conteudo.replace("Occurs concurrently to and after", "Ocorre junto com e depois de")
	conteudo = conteudo.replace("Occurs concurrently to", "Ocorre junto com")
	conteudo = conteudo.replace("Occurs immediately after", "Ocorre imediatamente depois de")
	conteudo = conteudo.replace("and during", "e durante")
	conteudo = conteudo.replace("Exact placement currently unknown", "Localização na linha do tempo desconhecida")
	conteudo = conteudo.replace("original trilogy", "trilogia original")
	conteudo = conteudo.replace("prequel trilogy", "trilogia prequela")

	conteudo = re.sub(r'\bde the\b', "de", conteudo)
	conteudo = conteudo.replace("[[Forum:SH", "[[:w:c:starwars:Forum:SH")

	print("Substituindo obras...")
	fix = fixes.fixes["obras"]
	for replacement in fix['replacements']:
		conteudo = re.sub(replacement[0], replacement[1], conteudo)

	refs = conteudo.split("<ref name=")[1:]
	for ref in refs:
		if (ref.find("</ref>") == -1):
			continue
		ref = ref.split("</ref>")[0]
		refName = ref.split(">")[0]
		if refName in refsTraduzidas:
			conteudo = conteudo.replace(ref, refsTraduzidas[refName])
		else:
			print("Nova referência: <ref name="+ref+"</ref>")
			resp = input("Traduzir? (Traduza ou aperte \"n\" para ignorar) ")
			if (resp=="n"):
				continue
			else:
				conteudo = conteudo.replace("<ref name="+ref+"</ref>", "<ref name="+refName+">"+resp+"</ref>")
		

	novoTexto += conteudo + fimTexto
	howManyFile = open("last_content_of_canon_media_timeline.txt", "w")
	howManyFile.write(paginaWookiee)
	howManyFile.close()
	pywikibot.showDiff(pagina.text, novoTexto)
	pagina.text = novoTexto
	if input("Ok? ([y]es/[n]o)").lower() == 'y':
		pagina.save(u'([[User:Thales César|Thales]]) 2.3 Expansão - Atualizando com conteúdo da Wookieepedia')
