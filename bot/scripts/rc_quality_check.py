# -*- coding: utf-8  -*-
"""
This script watches RecentChanges in order to check the quality of edits made

This will be integrated with another repo for actually checking the quality of an
edition
"""
import json

from pywikibot import pagegenerators

from bot.utils import swwsite as site


def get_creator(page):
    try:
        return page.getCreator()[0]
    except:
        return None

def main():
    edits = pagegenerators.RecentChangesPageGenerator(site=site, changetype="new")
    pages_contents = [
        {
            'title': p.title(),
            'text': p.text,
            'editor': get_creator(p)
        } for p in edits if int(p.namespace()) in [0, 114] and not p.isRedirectPage()]
    with open('rc_text.json', 'w+') as p:
        p.write(json.dumps(pages_contents))
