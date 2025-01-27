
import docutils.nodes as nodes
from sphinx.transforms import SphinxTransform
from sphinx.util.tags import Tags
from sphinx.addnodes import only
from sphinxdiff.nodes import (NodeDiffAdd, NodeDiffDel, NodeTagDiffIndex)
from sphinxdiff.dbg import dbg_print_ast
from sphinx.util.logging import getLogger


logger = getLogger(__name__)

class TransformOnly(SphinxTransform):
    
    default_priority = 406
    tags = ()
    
    def __init__(self, document, startnode=None):
        super().__init__(document, startnode)
        try:
            self.tags = self.config['sphinxdiff_tags']
        except KeyError as e:
            self.tags = ()
            
        self.labels = {}
        #print('TransformOnly.__init__', self.tags)

    def apply(self):
        #dbg_print_ast(self.document)

        for node in self.document.traverse(only):
            #print('TransformOnly:', node, node['expr'])
            expression = node['expr']
            adds = []
            dels = []
            for tag in self.tags:
                val = self.eval_expression_for_tag(expression, tag)
                #print('TransformOnly:', expression, tag, '->', val)
                if val == (True, False):
                    adds.append(tag)
                elif val == (False, True):
                    dels.append(tag)

            if adds and dels:
                raise NotImplementedError("TODO: Implement text to simultaneously added and deleted by (different) tags")
            elif adds:
                diff_node = NodeDiffAdd('')
                diff_node['tags'] = adds
            elif dels:
                diff_node = NodeDiffDel('')
                diff_node['tags'] = dels
            else:
                continue
            
            diff_node['label'] = self.create_label(adds, dels)
            #print("TransformOnly.apply creates label", diff_node['label'])
            diff_node.children = node.children
            diff_node.source = node.source
            diff_node.line = node.line
            for child in diff_node.children:
                child.parent = diff_node
            #up = node.parent
            node.replace_self(diff_node)
                
    def eval_expression_for_tag(self, expression, tagname):
        tagnames = list(self.app.builder.tags).copy()
        if tagname not in tagnames:
            return (True, True)
        
        tags_with = Tags(tagnames)
        tags_without = Tags([t for t in tagnames if t != tagname])
        
        try:
            return (tags_with.eval_condition(expression),
                    tags_without.eval_condition(expression))
        except Exception as err:
            msg = f'exception while evaluating only directive expression "{expression}" with and without "{tagname}": {err}'
            logger.warning(msg)
            return (True, True)
        
    def create_label(self, add_tags, del_tags):
        key = tuple(sorted(add_tags + del_tags))
        label_id = 1 + self.labels.get(key, 0)
        self.labels[key] = label_id
        parts = [self.env.docname, ':diff', str(label_id)]
        for tag in add_tags:
            parts.append('+')
            parts.append(tag)
        for tag in del_tags:
            parts.append('-')
            parts.append(tag)
        return ''.join(parts)


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
