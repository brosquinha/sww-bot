from pywikibot import Site

swwsite: Site = Site(fam="starwarsfandom", code='pt', user='BB-08')

def get_user_yes_or_no(message: str) -> bool:
	"""
	Gets user input to a yes or no question

	:param message: Message with question to the user
	:type message: String
	:return: Whether user answered with yes or not
	:rtype: Boolean
	"""
	return input(message).lower() == 'y'
