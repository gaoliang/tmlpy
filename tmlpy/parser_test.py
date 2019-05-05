import unittest

from tmlpy.parser import Parser


class TestParser(unittest.TestCase):
    cases = [
        {
            'name': "no-tags",
            'input': "plain",
            'output': "\x1b[0mplain\x1b[0m",
        },
        {
            'name': "basic",
            'input': "plain <red>red</red> plain",
            'output': "\x1b[0mplain \x1b[31mred\x1b[39m plain\x1b[0m",
        },
        {
            'name': "nesting",
            'input': "plain <red>red <bold>bold red</bold></red> plain <green>green</green> plain",
            'output': "\x1b[0mplain \x1b[31mred \x1b[1mbold red\x1b[0m\x1b[31m\x1b[39m plain \x1b[32mgreen\x1b[39m plain\x1b[0m",
        },
    ]

    def test_parse(self):
        for case in self.cases:
            parser = Parser()
            result = parser.parse(case['input'])
            self.assertEqual(result, case['output'])
