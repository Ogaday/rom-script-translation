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

    @vcr.use_cassette(
            "cassettes/test_bulk_translate_from_en_to_de.yml",
            filter_headers=["Ocp-Apim-Subscription-Key"]
        )
    def test_bulk_translate_from_en_to_gb(self):
        source_texts = [
                "Hello, world",
                "This is an exercise in coding",
                "I like writing tests"
            ]
        expected_texts = [
                "Hallo Welt",
                "Dies ist eine Übung in der Codierung",
                "Ich schreibe gerne Tests"
            ]
        translated_texts = translate(source_texts, from_="en", to="de")
        for translated, expected in zip(translated_texts, expected_texts):
            with self.subTest():
                self.assertEqual(translated, expected)
