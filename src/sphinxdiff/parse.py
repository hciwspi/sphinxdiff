'''Parsing functionality for sphinxdiff'''

from docutils.parsers.rst import directives, Directive
from sphinxdiff.nodes import (NodeDiffChange, NodeDiffAdd, NodeDiffDel,
                              NodeAddIn, NodeDelIn, NodeDiffChangeInline,
                              NodeTagDiffIndex)
from sphinxdiff.dbg import dbg_print_ast


def find_inline_delimiter(text):
    ## TODO: use errors
    errors = []
    regular = True
    pos = text.find('+|-')
    if 0 > pos:
        pos = text.find('-|+')
        regular = False
        if 0 > pos:
            raise ValueError('Delimiter "+|-" not found')
    added = text[: pos]
    deleted = text[pos + 3: ]
    if not regular:
        added, deleted = deleted, added

    return added, deleted, errors
    
def parse_diff_change_inl(role, rawtext, text, lineno, inliner,
                           options=None, content=None):
    #print('parse_diff_change_inl', role, rawtext, text, lineno, inliner)
    #doc = inliner.document ## during parser stage
    #dbg_print_ast(doc)
    #inliner.document(doc)
    #dbg_print_ast(inliner.parent.parent)
    
    #app = inliner.document.settings.env.app ## Fetch the Sphinx main app
    
    ## TODO: Parse inline text
    
    node = NodeDiffChangeInline(rawsource=rawtext, )
    node['role'] = role
    errors = []
    if role == 'change':
        added, deleted, errors = find_inline_delimiter(text)
        #print('parse_diff_change_inl', added, deleted, errors)
        node['new_text'] = added
        node['old_text'] = deleted
    elif role == 'add':
        node['new_text'] = text
    elif role == 'del':
        node['old_text'] = text

    return [node], errors

class DiffAddDelIn(Directive):
    required_arguments = 0
    optional_arguments = 2
    final_argument_whitespace = False
    option_spec = {'version': directives.unchanged,
                   'comment': directives.unchanged,
                  }
    has_content = True
    
    def run(self):
        directive_name = self.name
        version = self.options.get('version', '')
        comment_raw = self.options.get('comment', '')
        
        #print('DiffAddDelIn', directive_name, self.arguments, self.content)
        ## TODO: Parse inline content of comment_raw

        if directive_name == 'add_in':
            node = NodeAddIn('')
        elif directive_name == 'del_in':
            node = NodeDelIn('')
        else:
            return []
        node['version'] = ''.join(self.arguments)
        node['comment'] = comment_raw ## TODO: Convert inline markup
        
        if self.content:
            self.state.nested_parse(self.content, self.content_offset, node)
            ## TODO: Handle error messages from parsing content
            
        return [node]


class DiffAddDel(Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}
    has_content = True
    
    def run(self):
        directive_name = self.name
        if directive_name == 'add':
            node = NodeDiffAdd('')
        elif directive_name == 'del':
            node = NodeDiffDel('')
        else:
            return []
        
        #print('DiffAddDel', directive_name, self.arguments, self.content)
        
        if self.content:
            self.state.nested_parse(self.content, self.content_offset, node)
            ## TODO: Handle error messages from parsing content
            
        return [node]


class DiffChange(Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}
    has_content = True
    
    def split_content(self):
        ## TODO: Sort out where to put empty lines
        indent = None
        lastlinetype = '+'
        splitted = {'+': [], '-': []}
        errors= []
        
        for line in self.content:
            if not line.strip():
                splitted[lastlinetype].append(line)
            elif indent is None:
                lastlinetype = line[0]
                if lastlinetype not in ('+', '-'):
                    raise ValueError(
                        'Wrong line change prefix: {} not "+-"'.format(
                                                            lastlinetype))
                indent = 2 ## TODO: This is a fake
                splitted[lastlinetype].append(line[indent: ])
            else:
                lastlinetype = line[0]
                if lastlinetype not in ('+', '-'):
                    raise ValueError(
                        'Wrong line change prefix: {} not "+-"'.format(
                                                            lastlinetype))
                splitted[lastlinetype].append(line[indent: ])
        
        return splitted['+'], splitted['-'], errors
    
    def run(self):
        #print('DiffChange content', self.content)
        if not self.content:
            return []
        
        res = []
        added, deleted, errors = self.split_content()
        #print(added, deleted, errors)
        added_offset = self.content_offset
        deleted_offset = added_offset + len(added)  ## TODO: Check validity
        if added:
            node = NodeDiffAdd('')
            node['new_text'] = added
            ## TODO: Hack
            self.content.data = added
            self.state.nested_parse(self.content, self.content_offset, node)
            ## TODO: Handle error messages from parsing content
            res.append(node)
        if deleted:
            node = NodeDiffDel('')
            node['old_text'] = deleted
            ## TODO: Hack
            self.content.data = deleted
            self.state.nested_parse(self.content, self.content_offset, node)
            ## TODO: Handle error messages from parsing content
            res.append(node)
            
        return res



class TagDiffIndex(Directive):
    required_arguments = 0
    optional_arguments = 3
    final_argument_whitespace = True
    option_spec = {
        'title': directives.unchanged,
        'position': directives.unchanged,
        'latex_presentation': directives.unchanged,
        #'latex_index_columns': directives.unchanged,
        #'latex_super_entry': directives.unchanged,
        #'latex_index_in_toc': directives.unchanged,
        }
    has_content = False
    
    def _parse_position(self, text):
        if text is None:
            return None
        return {'begin': 'begin',
                'beginning': 'begin',
                'start': 'begin',
                'first': 'begin',
                'before': 'begin',
                'after': 'end',
                'last': 'end',
                'end': 'end',}.get(text.strip().lower(), None)
    
    def _parse_presentation(self, text):
        if text is None:
            text = 'definitionlist'
        return {'definitionlist': 'definitionlist', 
                'definition list': 'definitionlist', 
                'deflist': 'definitionlist', 
                'multiindex': 'multiindex', 
                'multind': 'multiindex', 
                'index': 'index', 
                'single index': 'index', 
                }.get(text.strip().lower(), None)
    
    def run(self):
        position = self._parse_position(self.options.get('position', None))
        title = self.options.get('title', 'Tag Changes Index')
        presentation = self._parse_presentation(
                self.options.get('latex_presentation', 'definitionlist'))
        #columns = int(self.options.get('latex_index_columns', 0))
        #super_entry = self.options.get('latex_super_entry', '')
        
        node = NodeTagDiffIndex('')
        if position:
            node['position'] = position
        node['title'] = title
        node['presentation'] = presentation
        #node['columns'] = columns
        #node['super_entry'] = super_entry
        
        document = self.state.document
        if position == 'end':
            document += node
        elif position == 'begin':
            pass
            ## TODO:insert first in document?
            
        return []
