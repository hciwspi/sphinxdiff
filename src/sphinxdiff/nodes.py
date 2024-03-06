'''Nodes for sphinxdiff'''

from docutils.nodes import Element, General, Inline


class NodeChangedIn(General, Element):
    def version(self): 
        return self['version']
        
    def comment(self): 
        return self['comment']

class NodeAddIn(NodeChangedIn):
    pass

class NodeDelIn(NodeChangedIn):
    pass

class NodeDiffChange(General, Element):
    def old(self): 
        return self['old_text'] if 'old_text' in self else ''
        
    def new(self): 
        return self['new_text'] if 'new_text' in self else ''
        
    #def comment(self): return self['comment']

class NodeDiffAdd(NodeDiffChange):
    pass

class NodeDiffDel(NodeDiffChange):
    pass
    
class NodeDiffChangeInline(NodeDiffChange, Inline):
    
    def role(self): 
        return self['role']




