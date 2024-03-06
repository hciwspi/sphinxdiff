.. _sphinxdiff-math:


Math example
============


A very popular application of something like *diff* we know from math: 
correcting proofs or calculations. 
In this case it is not so mutch about comparing two documents 
(a correct proof and the wrong argument) but to annotate the (failed) 
argument from its first error until it fails completely. 

Please note there are :math:`\LaTeX` packages avaliable that address these 
application:

* `changes <https://ctan.org/pkg/changes>`_
* `latexdiff <https://ctan.org/pkg/latexdiff>`_

You may want to use them in math mode.
The markup of ``sphinxdiff`` for math is rudimentary and only there for your 
convenience. 


Let's see some erroneous execises, plain and with annotations

Integration by parts
--------------------

Exercise: Find a closed formula for the indefinite integral

.. math:: \int e^x\cdot sin(x) dx 


Proof (flawed):

.. math:: 
   \int\underbrace{e^x}_{u'}\cdot \underbrace{sin(x)}_{v} dx 
      &= \left[ e^x\cdot sin(x)\right]
       + \int\underbrace{e^x}_{s}\cdot \underbrace{cos(x)}_{t'} dx \\
      &= \left[ e^x\cdot sin(x)\right]
       + \left[ e^x\cdot sin(x)\right]
       - \int e^x\cdot sin(x) dx \\
      &= 2\left[ e^x\cdot sin(x)\right]
       - \int e^x\cdot sin(x) dx \\
   \Rightarrow\ 2\int e^x\cdot sin(x) dx &= 2\left[ e^x\cdot sin(x)\right]\\
   \Rightarrow\ \int e^x\cdot sin(x) dx &= e^x\cdot sin(x) + Const
   
Corrected: 

.. math:: 
   \int\underbrace{e^x}_{u'}\cdot \underbrace{sin(x)}_{v} dx 
      &= \left[ e^x\cdot sin(x)\right]
        \Change{-}{+} \int\underbrace{e^x}_{s}\cdot 
                          \underbrace{cos(x)}_{t'} dx \\
      &= \left[ e^x\cdot sin(x)\right]
        \Change{-}{+} \left[ e^x\cdot sin(x)\right]
        \Change{+}{-} \int e^x\cdot sin(x) dx \\
      &= \Del{2\left[ e^x\cdot sin(x)\right]}
        \Change{+}{-} \int e^x\cdot sin(x) dx\\
   \Add{\Rightarrow 0 }&= \Add{0} \\
   \Del{\Rightarrow\ 2\int e^x\cdot sin(x) dx}
            & =\Del{2\left[ e^x\cdot sin(x)\right]}\\
   \Del{\Rightarrow\ \int e^x\cdot sin(x) dx} 
            &= \Del{e^x\cdot sin(x) + Const}
   
The corrected LaTeX code is somewhat messy:

.. code-block:: latex

   .. math:: 
      \int\underbrace{e^x}_{u'}\cdot \underbrace{sin(x)}_{v} dx 
         &= \left[ e^x\cdot sin(x)\right]
           \Change{-}{+} \int\underbrace{e^x}_{s}\cdot 
                             \underbrace{cos(x)}_{t'} dx \\
         &= \left[ e^x\cdot sin(x)\right]
           \Change{-}{+} \left[ e^x\cdot sin(x)\right]
           \Change{+}{-} \int e^x\cdot sin(x) dx \\
         &= \Del{2\left[ e^x\cdot sin(x)\right]}
           \Change{+}{-} \int e^x\cdot sin(x) dx \\
      \Add{\Rightarrow 0 }&=\Add{0} \\
         \Del{\Rightarrow\ 2\int e^x\cdot sin(x) dx}
            & =\Del{2\left[ e^x\cdot sin(x)\right]}\\
   \Del{\Rightarrow\ \int e^x\cdot sin(x) dx} 
            &= \Del{e^x\cdot sin(x) + Const}









