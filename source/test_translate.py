import unittest

import vcr

from source.translate import translate


class TestTranslate(unittest.TestCase):
    @vcr.use_cassette(
            "cassettes/test_translate_from_en_to_de.yml",
            filter_headers=["Ocp-Apim-Subscription-Key"]
        )
    def test_translate_from_en_to_gb(self):
        translated_text = translate("Hello, world!", from_="en", to="de")
        self.assertEqual(translated_text, "Hallo Welt!")
