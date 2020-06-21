# -*- coding: utf-8 -*-
"""
Updates Project:Apêndice de Tradução de Obras/JSON based on
local user-fixes' fixes['obras'] dictionary
"""
import json

from pywikibot import Page, showDiff

from bot.utils import get_user_yes_or_no, swwsite as site

def main():
    page = Page(site, "Star Wars Wiki:Apêndice de Tradução de obras/JSON")

    fixes = {}
    with open("bot/user-fixes.py") as f:
        exec(f.read()) # Can't import it normally because of naming and undefined variable

    if not 'obras' in fixes:
        raise Exception('Obras dictionary not found')

    fixes_json = json.dumps(fixes['obras'], ensure_ascii=False, indent=4)
    new_text = "<pre>{}</pre>".format(fixes_json)

    showDiff(page.text, new_text)
    if get_user_yes_or_no("Salvar?"):
        page.text = new_text
        page.save("([[User:Thales César|Thales]]) 2.2 Atualizado com novas informações")
