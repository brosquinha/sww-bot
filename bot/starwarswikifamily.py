from pywikibot import family

class StarWarsWikiFamily(family.Family):
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'starwarsfandom'
        self.langs = {
            'pt': 'starwars.fandom.com',
        }

    def protocol(self, code):
        return 'https'

    def scriptpath(self, code):
        return {
            'pt': '/pt',
        }[code]

    def version(self, code):
        return {
            'pt': u'1.19.24',
        }[code]
