'''Html writer for sphinxdiff
'''

from sphinxdiff.nodes import (NodeDiffChange, NodeDiffAdd, NodeDiffDel,
                              NodeAddIn, NodeDelIn, NodeDiffChangeInline)


def visit_changed_in_html(self, node):
    if isinstance(node, NodeAddIn):
        style = 'diff-add'
    elif isinstance(node, NodeDelIn):
        style = 'diff-del'
    else:
        style = 'diff'
    self.body.append('\n<div class="{}">'.format(style))

def depart_changed_in_html(self, node):
    self.body.append('\n</div>') 

def visit_change_node_html(self, node):
    if isinstance(node, NodeDiffAdd):
        style = 'diff-add'
    elif isinstance(node, NodeDiffDel):
        style = 'diff-del'
    else:
        style = 'diff'
    self.body.append('\n<div class="{}">'.format(style))

def depart_change_node_html(self, node):
    self.body.append('\n</div>')

def visit_inl_change_node_html(self, node):
    #from .dbg import dbg_print_ast
    #dbg_print_ast(self.document)
    
    #style = 'diff-' + node.role()
    added = node.new()
    deleted = node.old()
    
    if added:
        self.body.append('<span class="diff-add">')
        self.body.append(added)
        self.body.append('</span>')
    if deleted:
        self.body.append('<span class="diff-del">')
        self.body.append(deleted)
        self.body.append('</span>')

def depart_inl_change_node_html(self, node):
    pass

