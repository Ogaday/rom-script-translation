import io
import unittest

import vcr

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

    @vcr.use_cassette(
            "cassettes/test_script_translate_from_en_to_de.yml",
            filter_headers=["Ocp-Apim-Subscription-Key"]
        )
    def test_translate(self):
        with io.StringIO(sample) as stream:
            sc = Script.from_script(stream)
        s_de = sc.translate(to='de', batch_size=4)
        with self.subTest():
            self.assertEqual(len(s_de.lines), len(sc.lines))
        with self.subTest():
            expected = (
                    "Fragen Sie mich nach irgendetwas{03}über Rüstung."
                    "{1E}{00}"
                )
            self.assertEqual(s_de.lines[-1].content, expected)


class TestLine(unittest.TestCase):
    def test_str(self):
        two_lines = sample.split("\n")[:2]
        comment = two_lines[0].strip()
        content = two_lines[1].strip()
        line = Line(content, comment)
        self.assertEqual(str(line), "\n".join(two_lines))
