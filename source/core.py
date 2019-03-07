"""
This module contains ROM script primitives
"""
from source.translate import translate
from source.utils import annotated, deannotated


class Script:
    """
    Contains the contents of a script ripped from a ROM
    """
    def __init__(self, lines):
        """
        Create a Script instance from a list of lines
        """
        self.lines = lines

    @classmethod
    def from_script(cls, stream):
        """
        Parse a textual script to create a Script instance
        """
        lines = []
        for i, data in enumerate(stream.readlines()):
            if i % 2 == 0:
                comment = data.strip()
            else:
                content = data.strip()
                lines.append(Line(content, comment))

        return cls(lines)

    def to_script(self, stream):
        """
        Write out a script instance to textual script
        """
        stream.write(str(self))

    def __str__(self):
        return "\n".join(str(line) for line in self.lines) + "\n"

    def translate(self, to):
        """
        Translate the script to the target language.

        Contents of lines are translated, comments remain the same.

        Returns a new, translated instance of Script and this script is
        unmodified
        """
        contents = [annotated(line.content) for line in self.lines]
        translations = [deannotated(t) for t in translate(contents, to=to)]
        translated_lines = [
                Line(t, l.comment) for t, l in zip(translations, self.lines)
            ]
        return self.__class__(translated_lines)

    def roundtrip(self, via, n=1):
        """
        Roundtrip translation of the script.

        That is, translates the script to a target language and back again, n
        times.

        Returns a new, translated instance of Script and this script is
        unmodified
        """
        raise NotImplementedError


class Line:
    def __init__(self, content, comment):
        """
        Create a Line instance from a comment and a line of content
        """
        self.content = content
        self.comment = comment

    def translate(self, to):
        """
        Translate the content of a line to a new language.

        Returns a new translated instance of Line and this Line instance is
        unmodified
        """
        translated = translate(source_text=annotated(self.content), to=to)
        return self.__class__(
                content=deannotated(translated),
                comment=self.comment
            )

    def __str__(self):
        return f"{self.comment}\n{self.content}"
