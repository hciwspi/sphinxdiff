

def dbg_print_ast(ast):
    indent = ''
    buf = []
    _append_node_recurrently(buf, ast, indent)
    print(''.join(buf))

def _append_node_recurrently(appendto, node, indent):
    appendto.append('\n')
    appendto.append(indent)
    c = node.__class__.__name__
    s = str(node).replace('\n', ' ')
    if 100 < len(c) + len(s) + len(indent):
        s = s[: 80] + ' ...>'
    appendto.append('[' + c + '|' + s + ']')
    
    try:
        for child in node.children:
            _append_node_recurrently(appendto, child, indent + '  ')
    except AttributeError:
        pass
