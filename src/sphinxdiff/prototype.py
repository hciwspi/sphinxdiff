"""Command line tool 'diff'"""

import difflib
import re


class RstDifferSimpleParagraph(object):
    """Most simple rst differ only marking paragraphs.
    """

    def __init__(self, linejunk=None, charjunk=None):
        self.linejunk = linejunk
        self.charjunk = charjunk
        self.autochunk = None
    
    def compare(self, a, b):
        matcher = difflib.SequenceMatcher(self.linejunk, a, b, self.autochunk)
        res = []
        for tag, alo, ahi, blo, bhi in matcher.get_opcodes():
            print("***", tag, alo, ahi, blo, bhi)
            if tag == 'replace':
                 res += ['   - ' + t for t in a[alo: ahi]]
                 res += ['   + ' + t for t in b[blo: bhi]]
            elif tag == 'delete':
                res += ['   - ' + t for t in a[alo: ahi]]
            elif tag == 'insert':
                 res += ['   + ' + t for t in b[blo: bhi]]
            elif tag == 'equal':
                res += a[alo: ahi]
            else:
                raise ValueError('unknown tag %r' % (tag,))

        return res


__pat_leading_whitespace = re.compile(r'\s*')

def detect_indent(block):
    if not block:
        return block, ''
    indents = [__pat_leading_whitespace.match(line).group() for line in block]
    min_indent_len = min([len(i) for i in indents])
    if 0 == min_indent_len:
        return block, ''
    else:
        ## TODO: assert all (minimal) indents to be equal?
        min_indent = block[0][: min_indent_len]
        return [line[min_indent_len: ] for line in block], min_indent


class RstDifferLines(object):
    """All purpose diff algorithm based on line-by-line analysis 
    """

    def __init__(self, linejunk=None, charjunk=None, indent='   ', 
                 linebreakbefore=True, linebreakafter=True,):
        self.linejunk = linejunk
        self.charjunk = charjunk
        self.autochunk = None
        self.indent = indent
        self.linebreakbefore = linebreakbefore
        self.linebreakafter = linebreakafter
    
    def compare(self, a, b):
        matcher = difflib.SequenceMatcher(self.linejunk, a, b, self.autochunk)
        res = []
        for tag, alo, ahi, blo, bhi in matcher.get_opcodes():
            print("***", tag, alo, ahi, blo, bhi)
            if tag == 'replace':
                a_block, a_indent = detect_indent([t for t in a[alo: ahi]])
                b_block, b_indent = detect_indent([t for t in b[blo: bhi]])
                a_left, b_left, indent = self._split_indents(a_indent, b_indent)
                self.append_directive(res, 'change', indent)
                res += [a_left + a for a in a_block]
                res += [b_left + b for b in b_block]
            elif tag == 'delete':
                a_block, a_indent = detect_indent([t for t in a[alo: ahi]])
                a_left = a_indent + self.indent
                self.append_directive(res, 'del', a_indent)
                res += [a_left + a for a in a_block]
            elif tag == 'insert':
                b_block, b_indent = detect_indent([t for t in b[blo: bhi]])
                b_left = b_indent + self.indent
                self.append_directive(res, 'add', b_indent)
                res += [b_left + b for b in b_block]
            elif tag == 'equal':
                res += a[alo: ahi]
            else:
                raise ValueError(f'Unknown tag {tag:r}')
                
            if self.linebreakafter and tag != 'equal':
                res.append('\n')

        return res
    
    def append_directive(self, res, directive, indent):
        if self.linebreakbefore:
            res.append('\n')
        res.append(''.join([indent, '.. ', directive, '::\n']))

    
    def _split_indents(self, indent_a, indent_b):
        if indent_a == indent_b:
            indent = indent_a + self.indent
            return indent + '- ', indent + '+ ', indent_a
        min_len = min(len(indent_a), len(indent_b))
        min_a = indent_a[: min_len]
        min_b = indent_b[: min_len]
        if min_a != min_b:
            ## TODO: Search for minimum verbatimly indentical indent
            raise NotImplementedError(' '.join(["Mismatch indent:", 
                                                        repr(a_indent), 
                                                        "vs.", 
                                                        repr(b_indent)]))
        indent = min_a + self.indent
        return (indent + '- ' + indent_a[min_len: ], 
                indent + '+ ' + indent_b[min_len: ], 
                min_a)


class RstDiffer1(difflib.Differ):

    def __init__(self, ):
        super(RstDiffer1, self).__init__(linejunk=None, 
                                        charjunk=None)
        self.autochunk = False
        
    def compare(self, a, b):
        cruncher = difflib.SequenceMatcher(self.linejunk, a, b, self.autochunk)
        for tag, alo, ahi, blo, bhi in cruncher.get_opcodes():
            print("***", tag, alo, ahi, blo, bhi)
            if tag == 'replace':
                g = self._fancy_replace(a, alo, ahi, b, blo, bhi)
            elif tag == 'delete':
                g = self._dump('-', a, alo, ahi)
            elif tag == 'insert':
                g = self._dump('+', b, blo, bhi)
            elif tag == 'equal':
                g = self._dump(' ', a, alo, ahi)
            else:
                raise ValueError('unknown tag %r' % (tag,))

            yield from g




def diff_yields(a, b, minus_before_plus=True, indent='   '):
    diffs = difflib.ndiff(a.splitlines(keepends=True), 
                         b.splitlines(keepends=True), 
                         linejunk=None, charjunk=None)

    while diffs:
        line = next(diffs)
        print('***', line)
#         if line.startswith(' '):
#             yield line[2: ]
#         elif line.startswith('+') or line.startswith('-'):
#             yield indent + line
    yield from diffs

class DiffState(object):
    equal = 'equal'
    delete = 'delete'
    insert = 'insert'
    replace = 'replace'


class RelpaceLine(object):
    def __init__(self, line_del, info_del, line_ins, info_ins, indent=''):
        self.line_del = indent + line_del
        self.info_del = indent + info_del
        self.line_ins = indent + line_ins
        self.info_ins = indent + info_ins
    
    def __str__(self):
        return ''.join([self.line_del, self.line_ins])
        


def diff_ndiff(a, b, minus_before_plus=True, indent='   '):
    diffs = difflib.ndiff(a.splitlines(keepends=True), 
                          b.splitlines(keepends=True), 
                          linejunk=None, charjunk=None)
    if not diffs:
        return []
    res = []
    buffer = []
    state_prev = DiffState.equal
    
    try:
        line = next(diffs)
        while True:
            line2 = None
            if line.startswith(' '):
                state = DiffState.equal
                if state != state_prev:
                    res += buffer
                    buffer = []
                res.append(line[2: ])
            elif line.startswith('+'):
                state_prev = DiffState.insert
                if state != state_prev:
                    res += buffer
                    buffer = []
                buffer.append(indent + line)
            elif line.startswith('-'):
                ## We need to look ahead one line to detect the current state:
                ## It can be 'delete' or 'replace'.
                line2 = next(diffs)
                if line2.startswith('-'):
                    state = DiffState.delete
                elif line2.startswith('?'):
                    state = DiffState.replace
                if state != state_prev:
                    res += buffer
                    buffer = []

                if state == DiffState.replace:
                    buffer.append(RelpaceLine(line, line2, next(diffs), next(diffs), 
                                              indent))
                    line2 = None
                else:
                    buffer.append(indent + line)
            if line2 is None:
                line = next(diffs)
            else:
                line = line2
            state_prev = state
    except StopIteration as e:
        res += buffer

    return res

def diff_(a, b):
    differ = RstDiffer1()
    return differ.compare(a.splitlines(keepends=True), 
                          b.splitlines(keepends=True),)

def diff_unified(a, b, nr_context_lines=0, version1='version1', version2='version2'):
    return difflib.unified_diff(a.splitlines(keepends=True), 
                                b.splitlines(keepends=True), 
                                fromfile=version1, 
                                tofile=version2, 
                                n=nr_context_lines)


def diff(a, b, minus_before_plus=True, indent='   '):
    differ = RstDifferLines()
    diffs = differ.compare(a.splitlines(keepends=True), 
                           b.splitlines(keepends=True))
    return diffs
    


if __name__ == '__main__':
    import os
    import sys
    
    a = """Lorem ipsum dolor sit amet, consectetur adipisici elit, 
etc, etc, etc
sed eiusmod tempor incidunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, 
quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. 
Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint obcaecat cupiditat non proident, 
sunt in culpa qui officia deserunt mollit anim id est laborum."""

    b = """Mene mene tekel u-parsin,
...
sed eiusmod tempor incidunt ut labore et dolore magna aliqua. 
Quis quote iure reprehend  in voluptate velit esse eu nulla pariatur ipsissima. 
Excepteur sint obcaecat cupiditet non proident, 
sunt in culpa qui officia deserunt mollit anim id est laborum."""

    res = diff_ndiff(a, b)
    print(''.join([str(x) for x in res]))
    print('\n***\n')
    
    res = diff(a, b)
    print(''.join([str(x) for x in res]))
    
    print('\n***\n')
    
    
    c = """Programming languages used with Sphinx:

Python
   main implementation language.
   Development started in the 1990s.
   
TeX, LaTeX
   main writer for producing pdf.
   Developed in the 1970s.

HTML and Css
   for writing web pages
   Developed mostly in the 1990s.

JavaScript
   used with web pages for example math mode
   Appeared in mid 1990s.
"""

    d = """Programming languages used with Sphinx:

Python
   main implementation language.
   Development started in the 1990s.
   
TeX, LaTeX
   main writer for producing ``pdf``.
   Developed in the 1970s and 1980s.

HTML and Css
   for writing web pages
   Development started in the late 1980s.

JavaScript
   used with web pages for example math mode
   Appeared in mid 1990s.
"""

    res = diff(c, d)
    print(''.join([str(x) for x in res]))
    
    print('\n***\n')

