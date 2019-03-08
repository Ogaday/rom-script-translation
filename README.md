# Rom Translation

Helping my friend round-trip translate the script for a game, such as the one
produced by the
[Golden Sun Translation Toolkit](https://sourceforge.net/projects/gstoolkit/).

## Usage

Once your environment is set up, there is a CLI utility that can be run from
the root of the repo. It reads a script from stdin and pipes it to stdout. eg.
the following bash command first translates the contents of `data/script.txt`
to german, then to english and then saves it in `data/script_roundtrip.txt`.

```bash
$ cat data/script.txt | python -m translate de | python -m translate en > data/script_roundtrip.txt
```

## Script Format

The script for the game comes in a specific format.

```
#0000 Hello, world{00}
Hello, world{00}
#0001 Foo bar{03}{08}baz
Foo bar{03}{08}baz
...
#14EF Many lines later...
Many lines later...
```

Key points:
* Lines starting with `#` are comments
* Each line is numbered in hexadecimal
* The numbering of the lines should not change
* The script text contains artifacts such as `{03}` within the text. They
  represent different substitutions and markers within the text, such as names,
  newline characters etc. The artifacts interfere with the translation.

## Translation Service

I'm using the
[Microsoft Translation Service](https://azure.microsoft.com/en-us/services/cognitive-services/translator-text-api/)
on azure because they have a free tier. However, I'll structure the code so
it's relatively easy to swap out the translation backend.

In order to use the translation service, you need to set an environment
variable for the service key.

eg. on linux:

```bash
$ export TRANSLATION_TEXT_KEY=abcd1234...789xyz
```

## Development Environment

This code was developed on linux using Python 3.6. I suggest you use a python
[virtual environment](https://virtualenv.pypa.io/en/stable/) to manage the
dependencies.

For instance:

```bash
$ python -m virtualenv -p /path/to/python3.6 venv
```

Once you have the virtual env, you can run 

```bash
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt && pip install -r requirements-dev.txt
```

## Testing

```bash
$ ./run-tests.sh
```
