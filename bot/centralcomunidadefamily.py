from pywikibot import family

class CentralComunidadeFamily(family.Family):
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'centralcomunidade'
        self.langs = {
            'pt': 'comunidade.fandom.com',
        }

    def protocol(self, code):
        return 'https'

    def scriptpath(self, code):
        return {
            'pt': '',
        }[code]

    def version(self, code):
        return {
            'pt': u'1.19.24',
        }[code]
