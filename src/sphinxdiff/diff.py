'''Sphinx entry point for the sphinxdiff extension'''

import os
from sphinxdiff.nodes import (NodeDiffChange, NodeDiffAdd, NodeDiffDel,
                              NodeAddIn, NodeDelIn, NodeDiffChangeInline)
from sphinxdiff.parse import (parse_diff_change_inl, 
                              DiffChange, DiffAddDel, DiffAddDelIn)
from sphinxdiff.transforms import TransformOnly
from sphinxdiff.to_html import (visit_changed_in_html, 
                                depart_changed_in_html,
                                visit_change_node_html, 
                                depart_change_node_html, 
                                visit_inl_change_node_html, 
                                depart_inl_change_node_html,)
from sphinxdiff.to_latex import (visit_changed_in_latex, 
                                depart_changed_in_latex,
                                visit_change_node_latex, 
                                depart_change_node_latex, 
                                visit_inl_change_node_latex, 
                                depart_inl_change_node_latex,)

def nop(self, node): pass


class ConfigUpdater(object):
    """A callback for 'config-inited' event 
    
    1. It appends the sphinxdiff.sty to config.latex_additional_files
    2. It sets our special value config.sphinxdiff_tags to whatever the user
       specified in the conf.py. In case of errors it will be an empty tuple.
    """
    def __init__(self, texinputs):
        self.texinputs = texinputs
    
    def __call__(self, app, config):
        try:
            tags = config._raw_config['sphinxdiff_tags']
            config['sphinxdiff_tags'] = tuple(tags)
        except Exception:
            config['sphinxdiff_tags'] = ()

        extra_files = config['latex_additional_files']
        config['latex_additional_files'] = self.texinputs + list(extra_files)


def setup(app):
    """Initialization point of the directives / roles.
    """
    
    here = os.path.abspath(os.path.dirname(__file__))
    texinputs = os.path.join(here, 'texinputs')
    listtexinputs = [os.path.join(texinputs, f) for f in os.listdir(texinputs)]
    
    app.connect('config-inited', ConfigUpdater(listtexinputs))
    
    app.add_transform(TransformOnly)

    app.add_node(NodeAddIn,
                 html=(visit_changed_in_html, depart_changed_in_html),
                 latex=(visit_changed_in_latex, depart_changed_in_latex),
                 )
    app.add_node(NodeDelIn,
                 html=(visit_changed_in_html, depart_changed_in_html),
                 latex=(visit_changed_in_latex, depart_changed_in_latex),
                 )
                 
    app.add_node(NodeDiffChange,
                 html=(visit_change_node_html, depart_change_node_html),
                 latex=(visit_change_node_latex, depart_change_node_latex),
                 )
    app.add_node(NodeDiffAdd,
                 html=(visit_change_node_html, depart_change_node_html),
                 latex=(visit_change_node_latex, depart_change_node_latex),
                 )
    app.add_node(NodeDiffDel,
                 html=(visit_change_node_html, depart_change_node_html),
                 latex=(visit_change_node_latex, depart_change_node_latex),
                 )
    app.add_node(NodeDiffChangeInline,
                 html=(visit_inl_change_node_html, 
                       depart_inl_change_node_html),
                 latex=(visit_inl_change_node_latex, 
                        depart_inl_change_node_latex),
                 )

    app.add_role('change', parse_diff_change_inl)
    app.add_role('add', parse_diff_change_inl)
    app.add_role('del', parse_diff_change_inl)
    
    app.add_directive('change', DiffChange)
    app.add_directive('add', DiffAddDel)
    app.add_directive('del', DiffAddDel)
    
    app.add_directive('add_in', DiffAddDelIn)
    app.add_directive('del_in', DiffAddDelIn)
    

