import sys
from importlib import import_module

if __name__ == "__main__":
    script = sys.argv[1] if len(sys.argv) > 1 else input("Script to run: ")
    try:
        script_module = import_module('bot.scripts.{}'.format(script))
        script_module.main()
    except ModuleNotFoundError:
        print("Script {} does not exist".format(script))
