
import docutils.nodes as nodes
from sphinx.transforms import SphinxTransform
from sphinx.util.tags import Tags
from sphinx.addnodes import only
from sphinxdiff.nodes import (NodeDiffAdd, NodeDiffDel)
from sphinxdiff.dbg import dbg_print_ast
from sphinx.util.logging import getLogger


logger = getLogger(__name__)

class TransformOnly(SphinxTransform):
    
    default_priority = 406
    tags = ('production',
            )
    
    def __init__(self, document, startnode=None):
        super().__init__(document, startnode)
        # try:
        #     self.tags = self.config.values['sphinxdiff_tags']
        # except KeyError as e:
        #     self.tags = ()
       
        #print("Constructing TransformOnly", self.app.tags, type(self.app.tags), self.config.values)

    def register_tags(self, tags):
        if isinstance(tags, Tags):
            self.tags = tags.tags.keys()
        else:
            self.tags = tags
    
    def apply(self):
        #dbg_print_ast(self.document)
        
        for node in self.document.traverse(only):
            #print('TransformOnly:', node, node['expr'])
            expression = node['expr']
            for tag in self.tags:
                ## TODO: This heuristic does cover multiple tags in expression
                val = self.eval_expression_for_tag(expression, tag)
                #print('TransformOnly:', expression, tag, '->', val)
                if val == (True, False):
                    diff_node = NodeDiffAdd('')
                elif val == (False, True):
                    diff_node = NodeDiffDel('')
                else:
                    continue
                
                diff_node.children = node.children
                diff_node.source = node.source
                diff_node.line = node.line
                for child in diff_node.children:
                    child.parent = diff_node
                #up = node.parent
                node.replace_self(diff_node)
                break
                
                
    def eval_expression_for_tag(self, expression, tagname):
        tagnames = list(self.app.builder.tags.tags.keys())
        if tagname not in tagnames:
            return (True, True)
        
        tags_with = Tags(tagnames)
        tagnames.remove(tagname)
        tags_without = Tags(tagnames)
        
        try:
            return (tags_with.eval_condition(expression),
                    tags_without.eval_condition(expression))
        except Exception as err:
            msg = f'exception while evaluating only directive expression "{expression}" with and without "{tagname}": {err}'
            logger.warning(msg)
            return (True, True)


def _replace_node_by(node, new_node):     
    try:
        res = tags.eval_condition(node['expr'])
    except Exception as err:
        logger.warning(__('exception while evaluating only directive expression: %s'), err,
                       location=node)
        node.replace_self(node.children or nodes.comment())
    else:
        if res:
            node.replace_self(node.children or nodes.comment())        
