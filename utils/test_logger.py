from typing import NamedTuple, List, Any, Optional, Union, Hashable

def dictify_askey(item, key, ensuredict=False, defaults={}):
    if not isinstance(item, dict):
        if not ensuredict:
            return item
        ret = {key: item if item is not None else defaults.get(item, None)}
    return defaults | ret

def listify(item):
    if isinstance(item, list):
        return item
    else:
        return [item]

def stringify(item):
    if isinstance(item, str):
        return item
    else:
        return repr(item)

def get_possible_dictkey(d, key, dictify_as=None, ensuredict=False, default={}):
    if isinstance(d, dict):
        val = d.get(key, default.get(key, None))
    else:
        val = d if d is not None else default.get(key, None)
    return dictify_askey(val, dictify_as, ensuredict, defaults=default) if dictify_as is not None else val

class TestLogger:
    from os import get_terminal_size

    DEBUG = 3
    INFO = 2
    ERROR = 1
    QUIET = 0
    CRITICAL = 0
    SILENT = -1

    WRAP = 1
    TRUNCATE = 0
    NOWRAP = -1


    def __init__(self, cls, level, minwidth=10):
        self.name = cls.__name__
        self.level = level
        self._indent_levels = []
        self._indent_level = 0
        self._indent_overflow = 0
        self.minwidth = minwidth
        self.tabstop = 4
        self.update_termsize()

    def setLevel(self, level):
        self.level = level

    @property
    def indent_level(self):
        return self._indent_level

    @property
    def width(self):
        """Width of the space available for writing.
        
        A 1-character buffer is added to the end of the line in order to prevent weird terminal effects.
        """
        return self.COLUMNS - self.indent_level - 1

    def _get_underline(self, msg, uchar="-", onlyalpha=True, exclude=":"):

        def underline_char(char):
            if char in exclude:
                char = " "
            if onlyalpha and not char.isalpha():
                char = " "
            return char

        return [msg, "".join(map(underline_char, list(msg)))]

    def _get_header(self, char="=", margin_left=0, margin_right=0):
        return "".ljust(margin_left).ljust(self.width - margin_right, char)

    def debug(
            self, 
            *msgs, 
            indent: Optional[dict] = {}, 
            condition: Optional[bool] = True
        ):
        self.log(*msgs, level=self.DEBUG, indent=indent, condition=condition)

    def info(
            self, 
            *msgs, 
            indent: Optional[dict] = {},
            condition: Optional[bool] = True
        ):
        self.log(*msgs, level=self.INFO, indent=indent, condition=condition)

    def error(
            self, 
            *msgs, 
            indent: Optional[dict] = {},
            condition: Optional[bool] = True
        ):
        self.log(*msgs, level=self.ERROR, indent=indent, condition=condition)

    def critical(
            self, 
            *msgs, 
            indent: Optional[dict] = {},
            condition: Optional[bool] = True
        ):
        self.log(*msgs, level=self.CRITICAL, indent=indent, condition=condition)

    def log(
            self, 
            *msgs, 
            indent: Optional[dict] = {},
            condition: Optional[bool] = True,
            level: Optional[int] = None,
            sublevels: Optional[dict] = {},
        ):
        if level is None:
            level = self.INFO
        if self.level < level or not condition:
            return
        if len(kwargs) > 0:
            msgs.append(kwargs)
        for msg in msgs:
            self.print_item(None, msg, indent, level, group_context=sublevels)

    def print_item(
            self, 
            title: Optional[str] = None,
            item: Any,
            indent: int = 0,
            level: Optional[int] = -1,
            underline: Optional[str] = "-",
            inline: Optional[bool] = False,
            group_context: Optional[dict] = {}
        ):
        if self.level < level:
            return
        if title is not None:
            if underline is not None:
                tlines = self._get_underline(title, underline, exclude=":", onlyalpha=False)
            else:
                tlines = [title]
            if inlining:
                self._print_lineitem(tlines, listify(item), len(title), columnsep=2)
                return
            self.printlines(tlines)
        self.pushIndent(indent)
        try:
            items = item.items()
            self.print_group(item, **group_context)
        except (AttributeError, TypeError):
            self.printlines([stringify(item)])
        finally:
            self.popIndent()

    def print_group(
            self, 
            group: Union[dict, Any], 
            header: Optional[Union[dict, str]] = "=",
            footer: Optional[Union[dict, bool]] = "=",
            indent: Optional[Union[dict, int]] = {},
            level: Optional[Union[dict, int]] = {},
            underline: Optional[Union[dict, str]] = "-",
            inline: Optional[Union[dict, str]] = None
        ):

        header = dictify_as(header, "char", ensuredict=True)
        footer = dictify_as(footer, "char", ensuredict=True)

        if "char" in header:
            self.print_header(**header)
        context = {
                "indent": get_possible_dictkey
                }

        if not isinstance(group, dict):
            self.print_item(
                    group, 
                    get_possible_dictkey(indent, "indent", 0),
                    get_possible_dictkey(level, "level", -1)
                )
            return

        for title, item in group.items():
            ilevel = get_possible_dictkey(level, title, -1)
            iindent = get_possible_dictkey(indent, title, self.tabstop)
            iuchar = get_possible_dictkey(underline, title, None)
            iinline = get_possible_dictkey(inline, title, None)
            context = {"indent": indent.get(title, {}), "level": level.get(title, {}),
                       "underline": underline.get(title, {}), "inline": inline.get(title, {})}
            self.print_item(title, item, ilevel, indent=iindent, underline=iuchar, inline=iinline, group_context=context)
        if footer is not None:
            self.print_header(char=footer)

    def pushIndent(self, ilevel: Optional[int] = None):
        if ilevel is None:
            ilevel = self.tabstop
        self._indent_levels.append(ilevel)
        self.update_termsize()

    def popIndent(self):
        self._indent_levels.pop()
        self.update_termsize()

    def print(self, msg):
        prefix = (">"*self._indent_overflow).rjust(self.indent_level-1).ljust(self.indent_level)
        print(prefix + msg)

    def print_header(self, char="=", margin_left=0, margin_right=0):
        self.print(self._get_header(char, margin_left, margin_right))

    def printlines(self, lines, linebreak=1, maxlines=-1):
        self.update_termsize()
        if linebreak == self.WRAP:
            lines = self._breaklines(lines)
        elif linebreak == self.TRUNCATE:
            lines = [line[:self.width] for line in lines]
        if maxlines > 0 and 0 < len(lines) > maxlines:
            lines = lines[:maxlines]
            lines[-1] = lines[-1][:-3] + "..."
        for line in lines:
            self.print(line)

    def _breaklines(self, lines, continuation_group="| "):
        ret = []
        for line in lines:
            start = len(ret)
            while len(line) > 0:
                if len(ret) - start > 0:
                    line = continuation_group + line
                chunk, line = line[:self.width], line[self.width:]
                ret.append(chunk)
        return ret

    def _print_lineitem(
            self, 
            left: List[str], 
            right: List[str], 
            w_left: int, 
            columnsep: int, 
            trace_char=".",
            continuation_group="  > "
        ):
        right = " ".join(right)
        if any(map(lambda l: len(l) > w_left, left)):
            right = continuation_group + right
            left.extend(self._breaklines([right], continuation_group=continuation_group))
            self.printlines(left)
            return
        lines = []
        while len(right) > 0:
            if len(lines) > 0:
                trace_char = " "
            try:
                col1 = left.pop()
            except IndexError:
                col1 = continuation_group
                w_left = len(col1)
            w_right = self.width - w_left - columnsep
            lines.append(col1.ljust(w_left) + "".ljust(columnsep) + right[:w_right].rjust(w_right, trace_char))
        self.printlines(lines)

    def update_termsize(self):
        self.COLUMNS, self.ROWS = self.get_terminal_size()
        tot = 0
        for j, ilevel in enumerate(self._indent_levels):
            tot += ilevel
            if self.COLUMNS - tot < self.minwidth:
                self._indent_overflow = len(self._indent_levels) - j
                tot -= ilevel
                break
        self._indent_level = tot
