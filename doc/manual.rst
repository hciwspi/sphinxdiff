.. _sphinxdiff_man:


sphinxdiff manual
=================

Directives
----------


.. rst:directive:: change
   
   should be used for paragraphs that contain additions and deletions at the 
   same place. So this is the most common directive.
   The syntax is line based: Each line is prefix by "+ " for lines added and 
   "- " for lines deleted.

   .. code-block:: rst
   
      .. change::
          - This module completely tested and ready for operation
          + This module is thoroughy tested and recommented for operation.
          + Nevertheless we need more time to get it stable. 

.. rst:directive:: add
   
   Adding a block. For example adding some items to a list is possible by
   
   .. code-block:: rst
   
      Our services are
      
      * 
      
   To achieve the same with ``change`` would look like this 
   
   .. code-block:: rst
   
      Available are
      
      * apples
      .. change::
          + * oranges
          + * stawberries
      * pear


.. rst:directive:: del

   Deleting a block.
   
   .. code-block:: rst
   
      Dear all, 
      
      nothing has been done.
      .. del::
         We are terribly sorry.
      
   To achieve the same with ``changes`` would look like this
   
   .. code-block:: rst
   
      Dear all, 
      
      nothing has been done.
      .. change::
         - We are terribly sorry.
         
   
   

Roles / inline markup
---------------------

.. rst:role:: change

   Is for inline changing

   .. code-block:: rst
   
      ... suddenly we had to :change:`patch-|+rework` everything ...
      
      
.. rst:role:: add

   An inline version of ``add`` with only one argument (the added text). 
   Use this for brevity.

.. rst:role:: del

   An inline version of ``del`` with only one argument (the deleted text). 


Tools
-----

.. function:: diff(a, b, **kwds)

   Takes two .rst documents and produces a unified diff view 
   
   The algorithm soley uses the directive 'change' and operates line based. 
   So usually this is just the starting point for a finer diff view of the 
   document.
