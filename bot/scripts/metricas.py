# -*- coding: utf-8  -*-
"""
Counts all edits in RecentChanges and show metrics about edit in the last 3 months
"""
from datetime import datetime

import pywikibot
from pywikibot import pagegenerators

from bot.utils import swwsite as site

def main():
	rcp = site.recentchanges(end="2016-01-01T00:00:00Z")#, showBot=False)
	counting = {}
	for page in rcp:
		edit_time = datetime.strptime(page['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
		edit_year = edit_time.year
		edit_month = edit_time.month
		edit_time_index = edit_year, edit_month
		if edit_time_index not in counting:
			counting[edit_time_index] = 1
		else:
			counting[edit_time_index] += 1
	print(counting)