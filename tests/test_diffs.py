
from sphinxdiff import diff
import os.path
import logging


reference = """Lorem ipsum dolor sit amet, consectetur adipisici elit, 
etc, etc, etc
sed eiusmod tempor incidunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, 
quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. 
Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint obcaecat cupiditat non proident, 
sunt in culpa qui officia deserunt mollit anim id est laborum."""


def test_diff_01():
    a = reference
    b = """Mene mene tekel u-parsin,
...
sed eiusmod tempor incidunt ut labore et dolore magna aliqua. 
Quis quote iure reprehend  in voluptate velit esse eu nulla pariatur ipsissima. 
Excepteur sint obcaecat cupiditet non proident, 
sunt in culpa qui officia deserunt mollit anim id est laborum."""
    res = diff(a, b)
    logging.info(res)
    
    expected = [ '\n',
                 '.. change::\n',
                 '   - Lorem ipsum dolor sit amet, consectetur adipisici elit, \n', 
                 '   - etc, etc, etc\n', 
                 '   + Mene mene tekel u-parsin,\n', 
                 '   + ...\n', 
                 '\n',
                 'sed eiusmod tempor incidunt ut labore et dolore magna aliqua. \n', 
                 '\n',
                 '.. change::\n',
                 '   - Ut enim ad minim veniam, \n', 
                 '   - quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. \n', 
                 '   - Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. \n',
                 '   - Excepteur sint obcaecat cupiditat non proident, \n', 
                 '   + Quis quote iure reprehend  in voluptate velit esse eu nulla pariatur ipsissima. \n', 
                 '   + Excepteur sint obcaecat cupiditet non proident, \n', 
                 '\n',
                 'sunt in culpa qui officia deserunt mollit anim id est laborum.',]

    assert list(res) == list(expected)
    
def test_diff_dorian_gray():
    path_dorian_gray_1890 = 'doc/dorian_gray_1890_chapter_vii.rst'
    path_dorian_gray_1891 = 'doc/dorian_gray_1891_chapter_ix.rst'
    path_dorian_gray_diff = 'doc/dorian_gray_1890_vs_1891.rst'

    with open(path_dorian_gray_1890, 'rt') as file_1890:
        dorian_gray_1890 = file_1890.read()
    with open(path_dorian_gray_1891, 'rt') as file_1891:
        dorian_gray_1891 = file_1891.read()
    with open(path_dorian_gray_diff, 'rt') as file_diff:
        dorian_gray_diff = file_diff.read()

    res = diff(dorian_gray_1890, dorian_gray_1891)
    result = list(res[39: ])
    lines_expected = find_chapter_content(dorian_gray_diff.splitlines(True)) 
    is_same = all([a == b for a, b in zip(result, lines_expected)])
    
    if not is_same:
        basepath, extension = os.path.splitext(path_dorian_gray_diff)
        write_path = ''.join([basepath, '_draft', extension])
        with open(write_path, 'wt') as wf:
            wf.write(''.join(res))

        for res, exp in zip(result, lines_expected):
            assert res == exp

def find_chapter_content(raw):
    state_before_headline = True
    state_before_content = True
    res = []
    for line in raw: 
        if state_before_headline:
            if set(line) != {'-'}:
                continue
            else:
                state_before_headline = False
                continue
        elif state_before_content:
            if line.strip():
                continue
                
            state_before_content = False
        
        res.append(line)
    
    return res 
            
                
    
    
    
    

