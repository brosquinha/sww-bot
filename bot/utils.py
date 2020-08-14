import sys

from pywikibot import Site

swwsite: Site = Site(fam="starwarsfandom", code='pt', user='BB-08')
comunidadesite: Site = Site(fam="centralcomunidade", code='pt', user='BB-08')

def get_user_yes_or_no(message: str) -> bool:
	"""
	Gets user input to a yes or no question

	:param message: Message with question to the user
	:type message: String
	:return: Whether user answered with yes or not
	:rtype: Boolean
	"""
	return input(message).lower() == 'y'

def print_over_line(message: str, last_output_len: int = 0) -> int:
	"""
	Prints a new line over the last line printed.

	Usefull when analising a long list and the individual items are not
	important.

	:param message: Message to be printed over the current line
	:type message: String
	:param last_output_len: Lenght of the current printed message to be overwritten
	:type last_output_len: Integer
	:return: Lenght of given message (can be passed to next iteration of this function via last_output_len)
	:rtype: Integer
	"""
	sys.stdout.write("\r")
	sys.stdout.flush()
	sys.stdout.write(" "*last_output_len)
	sys.stdout.flush()
	sys.stdout.write("\r")
	sys.stdout.flush()
	sys.stdout.write(message)
	sys.stdout.flush()
	return len(message)
