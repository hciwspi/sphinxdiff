'''LaTeX writer for sphinxdiff
'''

from sphinxdiff.nodes import (NodeDiffChange, NodeDiffAdd, NodeDiffDel,
                              NodeAddIn, NodeDelIn, NodeDiffChangeInline)


def visit_changed_in_latex(self, node):
    if '1.3' != node.version():
        print("Do nothing for", node.version())
        return
    
    if node.comment():
        self.body.append('%\n\n\\marginpar{')
        self.body.append(node.comment())
        self.body.append('}\n')
        
    if isinstance(node, NodeAddIn):
        self.body.append('%\n\\SphinxDiffAdd{')
    elif isinstance(node, NodeDelIn):
        self.body.append('%\n\\SphinxDiffDel{')

def depart_changed_in_latex(self, node):
    if '1.3' != node.version():
        return
    
    if isinstance(node, (NodeDiffAdd, NodeDiffDel)):
        self.body.append('}\n')
    else:
        pass

# def visit_change_node_latex(self, node):
#     if isinstance(node, NodeDiffAdd):
#         self.body.append('%\n\\SphinxDiffAdd{')
#     elif isinstance(node, NodeDiffDel):
#         self.body.append('%\n\\SphinxDiffDel{')
#     else:
#         print("TODO: Split change into add / delete")
#
# def depart_change_node_latex(self, node):
#     if isinstance(node, (NodeDiffAdd, NodeDiffDel)):
#         self.body.append('}\n')
#     else:
#         pass

        
def visit_change_node_latex(self, node):
    if isinstance(node, NodeDiffAdd):
        self.body.append('%\n{\n\n\color{SphinxDiffAddText} ')
    elif isinstance(node, NodeDiffDel):
        self.body.append('%\n{\n\n\color{SphinxDiffDelText}')
    else:
        print("TODO: Split change into add / delete")


def depart_change_node_latex(self, node):
    if isinstance(node, NodeDiffAdd):
        self.body.append('}\n')
    elif isinstance(node, NodeDiffDel):
        self.body.append('}\n')

def visit_inl_change_node_latex(self, node):
    role = node.role()
    if role == 'add':
        self.body.append('\\SphinxDiffAdd{')
        self.body.append(node.new())
        self.body.append('}')
    elif role == 'del':
        self.body.append('\\SphinxDiffDel{')
        self.body.append(node.old())
        self.body.append('}')
    elif role == 'change':
        self.body.append('\\SphinxDiffChange{')
        self.body.append(node.new())
        self.body.append('}{')
        self.body.append(node.old())
        self.body.append('}')

def depart_inl_change_node_latex(self, node):
    pass

