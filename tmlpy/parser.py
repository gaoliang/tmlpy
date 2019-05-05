from tmlpy.tags import reset_fg, reset_bg, attr_tags, bg_tags, fg_tags, reset_all, attr_map


class Parser:
    def __init__(self):
        self.IncludeLeadingResets = True
        self.IncludeTrailingResets = True
        self.state = ParserState()
        self.result = ''

    def handle_tag(self, name):
        # handle close tags.
        if name.startswith('/'):
            name = name[1:]
            if name in fg_tags:
                self.result += self.state.set_fg(reset_fg)
                return True
            elif name in bg_tags:
                self.result += self.state.set_bg(reset_bg)
                return True
            elif name in attr_tags:
                self.result += self.state.set_attr(-attr_tags[name])
                return True
            else:
                return False

        # handle start tags.
        if name in fg_tags:
            self.result += self.state.set_fg(fg_tags[name])
            return True
        if name in bg_tags:
            self.result += self.state.set_bg(bg_tags[name])
            return True
        if name in attr_tags:
            self.result += self.state.set_attr(attr_tags[name])
            return True
        return False

    def parse(self, string):
        self.result = ''
        self.state = ParserState()
        if self.IncludeLeadingResets:
            self.result += reset_all

        inTag = False
        tagName = ''
        for char in string:
            if inTag:
                if char == ">":
                    if not self.handle_tag(tagName):
                        self.result += '<{}>'.format(tagName)
                    tagName = ''
                    inTag = False
                    continue
                tagName += char
                continue
            if char == "<":
                inTag = True
                continue

            self.result += char

        if self.IncludeTrailingResets:
            self.result += reset_all
        return self.result


class ParserState:

    def __init__(self):
        self.fg = ''
        self.bg = ''
        self.attrs = 0

    def set_fg(self, esc):
        if self.fg == esc:
            return ''
        self.fg = esc
        return esc

    def set_bg(self, esc):
        if self.bg == esc:
            return ''
        self.fg = esc
        return esc

    def set_attr(self, attr):
        output = ''
        if attr < 0:
            output = reset_all + self.fg + self.bg

        self.attrs = attr + self.attrs
        for attr, esc in attr_map.items():
            if self.attrs & attr > 0:
                output += esc
        return output


if __name__ == "__main__":
    parser = Parser()
    print(parser.parse("<red>this text is <bold>red</bold></red> and the following is <green>not red</green>"))
