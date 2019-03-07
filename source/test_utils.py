import unittest

from source.utils import annotated, deannotated, paginate


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


class TestPagination(unittest.TestCase):
    def test_pagination_max_lines(self):
        lines = [
                "0000000000",
                "1111111111",
                "2222222222",
                "3333333333",
            ]
        chunks = []
        for page in paginate(lines, max_buffer=100, max_lines=3):
            chunks.append(page)
        with self.subTest():
            self.assertEqual(len(chunks[0]), 3)
        with self.subTest():
            self.assertEqual(len(chunks[1]), 1)

    def test_pagination_max_buffer(self):
        lines = [
                "0000000000",
                "1111111111",
                "2222222222",
                "3333333333",
            ]
        chunks = []
        for page in paginate(lines, max_buffer=25, max_lines=100):
            chunks.append(page)
        with self.subTest():
            self.assertEqual(len(chunks[0]), 2)
        with self.subTest():
            self.assertEqual(len(chunks[1]), 2)

    def test_pagination_no_max(self):
        lines = [
                "0000000000",
                "1111111111",
                "2222222222",
                "3333333333",
            ]
        chunks = []
        for page in paginate(lines, max_buffer=100, max_lines=100):
            chunks.append(page)
        with self.subTest():
            self.assertEqual(len(chunks), 1)
        with self.subTest():
            self.assertEqual(len(chunks[0]), 4)

    def test_pagination_example(self):
        lines = [
                '000000',
                '1111',
                '222222222',
                '3',
                '4',
                '5555555555',
                '66666666',
                '77',
                '88888888',
                '9',
                '0000000',
                '1',
                '222222222',
                '33333333',
                '4444',
                '55555555',
                '6666666',
                '77777777',
                '8',
                '99'
            ]

        max_buffer = 15
        max_lines = 3
        paged = []
        for page in paginate(lines, max_buffer, max_lines):
            with self.subTest():
                self.assertLessEqual(len(page), max_lines)
            with self.subTest():
                self.assertLessEqual(len(''.join(page)), max_buffer)
            paged += page
        with self.subTest():
            self.assertEqual(''.join(lines), ''.join(paged))
