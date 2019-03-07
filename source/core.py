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
        translated_lines = []

        for page in self.paginate():
            contents = [line.content for line in page]
            comments = [line.comment for line in page]
            source_texts = [annotated(content) for content in contents]
            translated_contents = [
                    deannotated(text) for text in
                    translate(source_text=source_texts, to=to)
                ]
            translated_page = [
                    Line(content, comment) for content, comment in
                    zip(translated_contents, comments)
                ]
            translated_lines += translated_page
        return self.__class__(translated_lines)

    def paginate(self, max_buffer=5000, max_lines=100):
        """
        Iterate through chunks of lines to fit the translation requests

        The Microsoft azure request has limitations on size:
            * Each request must have no more than 100 lines to translate
            * The combined characters of each request must be less than 5000

        TODO:
            * This should be called within the microsoft specific
              `translate` function, as that's why this logic must be
              implemented.
        """
        start = 0
        stop = 0

        while stop < len(self.lines):
            if len(annotated(self.lines[stop].content)) > max_buffer:
                raise Exception('A line is too long')
            buffer_size = len(
                    ''.join(
                        [
                            annotated(line.content)
                            for line in self.lines[start:stop + 1]
                        ]
                    )
                )
            num_lines = len(self.lines[start:stop + 1])
            if buffer_size > max_buffer or num_lines > max_lines:
                yield self.lines[start:stop]
                start = stop
            stop += 1
        else:
            yield self.lines[start:stop]

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
