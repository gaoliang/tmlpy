from tmlpy.parser import Parser


class Tml:
    def __init__(self):
        self.parser = Parser()

    def print(self, *args, sep=' ', end='\n'):
        result = self.parser.parse(sep.join(map(str, args)))
        print(result, end=end)

    def parse(self, string):
        return self.parser.parse(string)
