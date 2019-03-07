"""
Entrypoint for the translation modules

Reads a script from stdin and pipes the translated script to stdout

Example:

    cat script.txt | python -m translate de | python -m translate en

"""
import sys

from source.core import Script


if __name__ == "__main__":
    try:
        lang = sys.argv[1]
    except IndexError:
        lang = 'de'
    s = Script.from_script(sys.stdin)
    s_t = s.translate(to=lang)
    sys.stdout.write(str(s_t))
