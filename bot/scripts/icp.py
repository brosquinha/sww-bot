# -*- coding: utf-8  -*-
"""
Gets the latest 100 pages created from Recent Changes and counts how many of those
were created with ICP's help.
"""
import pywikibot
from pywikibot import pagegenerators

from bot.utils import swwsite as site

def main():
	gen = pywikibot.pagegenerators.RecentChangesPageGenerator(
		namespaces=0, showRedirects=False, changetype="new", site=site)
	i = 0
	icp = 0
	for page in gen:
		if (i > 99):
			break
		print(page.title())
		if (page.text.find("<!-- Artigo gerado pelo ICP -->") > -1):
			icp += 1
		i += 1
	print("\n{0} de {1} criadas com ICP ({2:.2f}%)".format(icp, i, (icp/i)*100))
