import io
import unittest

from source.core import Script, Line


sample = (
        "#0CC3 Let me give you this{03}{14}{01} as a token{03}of my gratitude."
        "{01}{00}\n"
        "Let me give you this{03}{14}{01} as a token{03}of my gratitude."
        "{01}{00}\n"
        "#0CC4 So who gets this{03}{14}{01}?{1E}{00}\n"
        "So who gets this{03}{14}{01}?{1E}{00}\n"
        "#0CC5 What! You don't want it?{01}{00}\n"
        "What! You don't want it?{01}{00}\n"
        "#0CC6 Ask me anything{03}about armor.{1E}{00}\n"
        "Ask me anything{03}about armor.{1E}{00}\n"
)


class TestScript(unittest.TestCase):
    def test_from_script(self):
        with io.StringIO(sample) as stream:
            sc = Script.from_script(stream)
            self.assertEqual(len(sc.lines), 4)

    def test_to_script(self):
        with io.StringIO(sample) as stream:
            sc = Script.from_script(stream)
        with io.StringIO() as stream:
            sc.to_script(stream)
            self.assertEqual(stream.getvalue().strip(), sample.strip())


class TestLine(unittest.TestCase):
    def test_str(self):
        two_lines = sample.split("\n")[:2]
        comment = two_lines[0].strip()
        content = two_lines[1].strip()
        line = Line(content, comment)
        self.assertEqual(str(line), "\n".join(two_lines))
