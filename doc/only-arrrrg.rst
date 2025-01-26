
======================================
  Demo: diff view on only directives
======================================


This page will show how ``sphinxdiff`` can be used to produce nice diff views
on sphinx's ``only`` directives. 




   
   
.. only:: not arrrrg
   
   Who would say arrrrg?

.. only:: arrrrg
   
   Beware of the killer rabbit!
   
.. only arrrrg and neverset

   This paragraph will not show in the documentation (when build with only the 
   tag ``arrrrg`` active)
   
.. only:: not(arrrrg and neverset)

   One disadvantage of using ``only`` directives to highlight changes in a 
   document comes from the design of ``only`` directives: They just operate on 
   whole paragraphs.
   
   So using them for tracking changes requires a workaround.
   On can repeat every paragraph with changes, once guarded with 
   ``.. only:: not <tag>`` (giving the former version of the whole paragraph) 
   and also the whole new paragraph under ``.. only:: <tag>``.

The relevant part of this demo in source is:

.. code-block:: rst

   .. only:: not arrrrg
      
      Who would say arrrrg?
   
   .. only:: arrrrg
      
      Beware of the killer rabbit!
      
   .. only arrrrg and neverset
   
      This paragraph will not show in the documentation (when build with only the 
      tag ``arrrrg`` active)
      
   .. only:: not(arrrrg and neverset)
   
      One disadvantage of using ``only`` directives to highlight changes in a
      ...
