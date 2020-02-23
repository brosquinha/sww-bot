# -*- coding: utf-8  -*-
"""
This script counts a given user contributions in order to check if this user can be awarded some
Star Wars Wiki medals (https://starwars.fandom.com/pt/wiki/Star_Wars_Wiki:Medalhas)
"""
import getopt
import sys
import time
import urllib
from datetime import datetime

import pywikibot
from pywikibot import pagegenerators

from bot.utils import get_user_yes_or_no, print_over_line
from bot.utils import swwsite as site


def main():
	username = ''
	while (username == ''):
		username = input("Usuário: ")
	should_count_100K =  get_user_yes_or_no(
		"Contar medalha de 100K? Ela pode demorar bastaaante em usuários com muitas edições... ([y]es/[n]no) ")
	user = pywikibot.User(site, username)
	if not user.exists():
		print("Usuário {} não existe".format(username))
		return
	contributions = user.contributions(total=user.editCount(), namespaces=[0])

	start_date_for_medals = datetime.strptime("2017-12-16T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
	contributions_sum = 0
	canon_pages_edited = 0
	canon_pages_created = 0
	progress_counter = 0
	output_str_len = 0
	for contrib in contributions:
		progress_counter = progress_counter + 1
		page = contrib[0]
		revisionID = contrib[1]
		editTime = contrib[2]
		paginasContadas = []
		paginasEditadas = 0
		editTimeDT = datetime.strptime(editTime.isoformat(), "%Y-%m-%dT%H:%M:%SZ")
		diferencaTime = editTimeDT - start_date_for_medals
		
		if (should_count_100K):
			page_history = page.revisions()
			revidAnt = 0
			for rev in page_history:
				if (rev.revid == revisionID):
					revidAnt = revisionID
				elif (revidAnt != 0):
					revidAnt = rev.revid
					break
			if (revidAnt == revisionID):
				diffLen = (len(page.getOldVersion(revisionID).encode('utf-8')))
			else:
				diffLen = (len(page.getOldVersion(revisionID).encode('utf-8')) - len(page.getOldVersion(revidAnt).encode('utf-8')))
			if (diffLen > 0 and max(editTimeDT, start_date_for_medals) == editTimeDT):
				contributions_sum = contributions_sum + diffLen
		output_str_len = print_over_line(
			message="Progresso: {0:.3f}%".format((progress_counter/(user.editCount()*1.0))*100),
			last_output_len=output_str_len
		)
		content = page.text
		if (content.lower().find("{{eras") > -1):
				eras = content.lower().split("{{eras")[1].split("}}")[0]
				if (eras.find("real") > -1):
					continue
		canon_pages_edited += 1
		if (page.oldest_revision.revid == revisionID):
			canon_pages_created += 1
		
	article_list = ["Luke Skywalker", "Leia Organa", "Rey", "Finn", "Kylo Ren", "Anakin Skywalker",
		"Ahsoka Tano", "Obi-Wan Kenobi", "Yoda", "Estrela da Morte"]
	for article in article_list:
		page = pywikibot.Page(site, article)
		page_history = page.revisions()
		revidAnt = 0
		article_contrib_sum = 0
		contrib_bytes = 0
		for rev in page_history:
			if (rev.user == username and contrib_bytes == 0):
				contrib_bytes = len(page.getOldVersion(rev.revid).encode('utf-8'))
			elif (rev.user != username and contrib_bytes != 0):
				article_contrib_sum = (article_contrib_sum +
					(contrib_bytes - len(page.getOldVersion(rev.revid).encode('utf-8'))))
				contrib_bytes = 0
		article_contrib_sum += contrib_bytes
		print("Soma de contribuições em {}: {}".format(article, article_contrib_sum))
		
	print("Soma de contribuições depois da introdução 100k:", contributions_sum)
	print("\nMedalhas ganhas:")
	if (contributions_sum > 100000):
		print("Medalha de Honra 100k")
	print(canon_pages_created , "páginas canônicas criadas")
	print(canon_pages_edited , "edições em artigos canônicos")
