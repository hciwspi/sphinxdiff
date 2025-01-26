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
    
    def tags(self): 
        return self['tags'] if 'tags' in self else []
    
    def label(self): 
        return self['label'] if 'label' in self else ''
        
    #def comment(self): return self['comment']

class NodeDiffAdd(NodeDiffChange):
    pass

class NodeDiffDel(NodeDiffChange):
    pass
    
class NodeDiffChangeInline(NodeDiffChange, Inline):
    
    def role(self): 
        return self['role']

class NodeTagDiffIndex(General, Element):

    def position(self): 
        return self['position'] if 'position' in self else None
    
    def title(self): 
        return self['title'] if 'title' in self else ''
    
    def presentation(self): 
        return self['presentation']

