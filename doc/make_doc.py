
if __name__ == '__main__':
    import sys, os, argparse
    from sphinx.cmd.build import build_main
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tag', dest='tags', action='append', 
                        help='Define tag for "only" directive')
    args = parser.parse_args()
    if args.tags is None:
        tags = []
    else:
        tags = [a for tag in args.tags for a in ['-t', tag]]
        
    print("Building with tags:", args.tags)
    
    ## Path to where make_doc operates:
    workingdir = os.path.dirname(os.path.abspath(__file__))
    
    ## Path to project base directory (usually github project level)
    basedir = os.path.dirname(workingdir)
    
    ## Path to (top level) document sources (.rst files)
    docdir = os.path.join(basedir, 'doc')
    
    ## Technical paths to shared doctree files and other build files
    builddir = os.path.join(workingdir, 'build')    
    doctreesdir = os.path.join(builddir, os.path.join('doctrees'))
    
    htmlbuild = os.path.join(builddir, 'html') 
 
    res = build_main(argv=['-b', 'html',
                           '-d', doctreesdir,
                           *tags,
                           docdir,
                           htmlbuild,
                           ])
    if 0 != res:
        print("html generation failed:", res)
        sys.exit(res)
    print("\nhtml generation done\n")
 
    res = build_main(argv=['-b', 'latex',
                           '-d', doctreesdir,
                           *tags,
                           docdir, 
                           os.path.join(builddir, 'latex'),
                           ])
    if 0 != res:
        print("latex generation failed:", res)
        sys.exit(res)
     
    print('Done')
