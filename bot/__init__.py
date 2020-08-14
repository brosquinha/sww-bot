import os
os.environ["PYWIKIBOT_NO_USER_CONFIG"] = "2"
import pywikibot

from .centralcomunidadefamily import CentralComunidadeFamily
from .starwarswikifamily import StarWarsWikiFamily

import warnings
warnings.simplefilter("ignore", category=pywikibot.exceptions._NotImplementedWarning)

pywikibot.Family._families["starwarsfandom"] = StarWarsWikiFamily()
pywikibot.Family._families["centralcomunidade"] = CentralComunidadeFamily()

site = pywikibot.Site(fam="starwarsfandom", code='pt', user='BB-08')
