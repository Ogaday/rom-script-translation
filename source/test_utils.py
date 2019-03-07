import unittest

from source.utils import annotated, deannotated


class TestAnnotation(unittest.TestCase):
    def test_annotate(self):
        text = "Ask me anything{03}about armor.{1E}{00}"
        expected = (
                'Ask me anything<div class="notranslate">{03}</div>about '
                'armor.<div class="notranslate">{1E}</div><div '
                'class="notranslate">{00}</div>'
            )
        self.assertEqual(annotated(text), expected)

    def test_deannotate(self):
        text = (
                'Fragen Sie mich nach irgendetwas<div class="notranslate">'
                '{03}</div>über Rüstung.<div class="notranslate">{1E}'
                '</div><div class="notranslate">{00}</div>'
            )
        expected = 'Fragen Sie mich nach irgendetwas{03}über Rüstung.{1E}{00}'
        self.assertEqual(deannotated(text), expected)
        pass

    def test_roundtrip(self):
        text = "Ask me anything{03}about armor.{1E}{00}"
        self.assertEqual(text, deannotated(annotated(text)))
