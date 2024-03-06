
==============
  sphinxdiff 
==============


This Python package provides 

* sphinx extension ``sphinxdiff`` for producing diff views of two documents
* a tool for diffing ``rst`` files.


The sphinx extension provides directives and roles for documenting changes 
in documentation build by sphinx.

The tool are for producing an diffing draft to start with two files.  
The process of producing a diff view is of course quite complex and involves a 
lot of choices (granularity of detail, grouping changes, reporting technical or 
invisible differences, ...) which requires an author.  
Therefore the tool (though highly configurable) is not aiming to the job 
completely automatically but to give the editor a headstart and a clear view on 
the changes.


Installing
==========

Install as Python package any way you like for example by pip::

   pip install sphinxdiff


Usage
=====

To use the sphinx extension add "sphinxdiff" to the list of ``extensions`` in 
the sphinx config file.  For example::

   extensions = [
       'sphinx.ext.intersphinx',
       'sphinx.ext.mathjax',
       'sphinx.ext.autodoc',
       'sphinxdiff',
       ]


Documentation
=============


TODO: link to readthedocs 
