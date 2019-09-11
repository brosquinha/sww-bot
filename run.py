import sys

from bot.scripts import aparicoes
from bot.scripts import emuso
from bot.scripts import linha_do_tempo

if __name__ == "__main__":
    script = sys.argv[1] if len(sys.argv) > 1 else input("Script to run: ")
    try:
        eval(script).main()
    except NameError:
        print("Script {} does not exist".format(script))
