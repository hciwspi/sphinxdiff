'''LaTeX writer for sphinxdiff
'''

import re
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


def register_index(latex_translator, node):
    env = latex_translator.builder.env
    if not hasattr(env, 'sphinxdiff_tag_index'):
        env.sphinxdiff_tag_index = {}
        
    for tag in node.tags():
        labels = env.sphinxdiff_tag_index.setdefault(tag, [])
        labels.append(node.label())
    
        
def visit_change_node_latex(self, node):
    self.body.append('%\n{')
    self.body.append('\n\n') # Start a new paragraph
    if node.label():
        label = ''.join((r'\label{\detokenize{', node.label(), '}}'))
        self.body.append(label)
        register_index(self, node)
    #print(f'{{\\hyperref[\\detokenize{{{node.label()}}}]{{\\pageref*{{\\detokenize{{{node.label()}}}}}}}}},')
    if isinstance(node, NodeDiffAdd):
        self.body.append(r'\color{SphinxDiffAddText} ')
    elif isinstance(node, NodeDiffDel):
        self.body.append(r'\color{SphinxDiffDelText}')
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


def docclass_has_chapter(latex_translator):
    try:
        docclass = latex_translator.document['docclass']
    except KeyError:
        ## legacy sphhi 2.xx support
        docclass = latex_translator.document.settings.docclass
        
    return docclass not in ('article', 'howto', 'azhowto')


def top_sections(latex_translator):
    if docclass_has_chapter(latex_translator):
        return (r'\chapter', r'\section', r'\subsection')
    return (r'\section', r'\subsection', r'\subsubsection', )
 
  
_pat_underscore = re.compile(r'([^\\])_')

def append_deflist_tag_index(body, tag_index, section_type, title):
    if not tag_index:
        return
 
    if title.strip():
        ## TODO: Have an option to set the *: latex_index_in_toc?
        body.append(f'\n\n{section_type}*{{{title}}}\n')
        body.append(r'\label{\detokenize{sphinxdiff-tag-change-index}}') 
    body.append('\n\n\\begin{description}')
    
    for tag in sorted(tag_index.keys()):
        labels = tag_index[tag]
        tag = _pat_underscore.sub(r'\1\_', tag)
        if labels:
            body.append(f'\n\\item[{tag}]')
            for label in labels:
                body.append(f"""
    {{\\hyperref[\\detokenize{{{label}}}]{{\\pageref*{{\\detokenize{{{label}}}}}}}}},""")
        
    body.append('\n\\end{description}')


def visit_tag_index_node_latex(latex_translator, node):
    env = latex_translator.builder.env
    if not hasattr(env, 'sphinxdiff_tag_index'):
        return
    
    position = node.position()
    if position is None:
        return
    
    ## TODO implement other options - like multiindex
    if node.presentation() != 'definitionlist':
        print("Tag Diff Index presentation option", node.presentation(), 
              "not implemented yet. Using 'definitionlist' instead.")
    
    buffer = []
    append_deflist_tag_index(buffer, 
                             env.sphinxdiff_tag_index, 
                             top_sections(latex_translator)[1], 
                             node.title())
    index_src = ''.join(buffer)
    
    if not index_src.strip():
        return 
    
    if position == 'end': 
        ## Place tag index after the index. 
        ## Recommended by sphinx documentation on latex element configuration: 
        ## See https://www.sphinx-doc.org/en/master/latex.html
        ## section on ``printindex``.
        latex_translator.elements['printindex'] = '\n'.join((
                latex_translator.elements['printindex'],
                r'\newpage', 
                index_src))
    elif position == 'start': 
        print('option "start" not implemented for ') 
        #body.append('\n\\newpage'



