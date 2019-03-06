"""
This module contains ROM script primitives
"""
from source.translate import translate, bulk_translate
from source.utils import annotated, deannotated, paginate


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

    def translate(self, to, batch_size=50):
        """
        Translate the script to the target language.

        Contents of lines are translated, comments remain the same.

        Returns a new, translated instance of Script and this script is
        unmodified
        """
        translated_lines = []

        for page in paginate(self.lines, batch_size):
            contents = [line.content for line in page]
            comments = [line.comment for line in page]
            source_texts = [annotated(content) for content in contents]
            translated_contents = [
                    deannotated(text) for text in
                    bulk_translate(source_texts=source_texts, to=to)
                ]
            translated_page = [
                    Line(content, comment) for content, comment in
                    zip(translated_contents, comments)
                ]
            translated_lines += translated_page
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
