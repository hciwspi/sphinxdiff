.. _sphinxdiff-faust:


Verse Example: Urfaust versus Faust I
=====================================

Johann Wofgang Goethe's tragedy "Faust" has been published twice, 
first in *Sturm und Drang* and later by the *Weimarer classic* Goethe. 
We abuse the first scene to demonstrate ``sphinxdiff``.


First version: Urfaust (1774)
-----------------------------

| NACHT.
| *In einem hochgewölbten engen gothischen Zimmer.*

|
| **Faust** *unruhig auf seinem Sessel am Pulten.*
| Hab nun, ach! die Philosophey,
| Medizin und Juristerey
| Und leider auch die Theologie
| Durchaus studirt mit heisser Müh.
| Da steh ich nun, ich armer Thor,
| Und binn so klug als wie zuvor.
| Heisse Docktor und Professor gar
| Und ziehe schon an die zehen Jahr
| Herauf, herab und quer und krumm
| Meine Schüler an der Nas herum
| Und seh, dass wir nichts wissen können:
| Das will mir schier das Herz verbrennen.
| Zwar binn ich gescheuter als alle die Laffen
| Docktors, Professors, Schreiber und Pfaffen,
| Mich plagen keine Skrupel noch Zweifel,
| Fürcht mich weder vor Höll noch Teufel.
| Dafür ist mir auch all Freud entrissen,
| Bild mir nicht ein, was rechts zu wissen,
| Bild mir nicht ein, ich könnt was lehren
| Die Menschen zu bessern und zu bekehren,
| Auch hab ich weder Gut noch Geld
| Noch Ehr und Herrlichkeit der Welt:
| Es mögt kein Hund so länger leben
| Drum hab ich mich der Magie ergeben,
| Ob mir durch Geistes Krafft und Mund
| Nicht manch Geheimniss werde kund,
| Dass ich nicht mehr mit saurem Schweis
| Rede von dem, was ich nicht weis,
| Dass ich erkenne, was die Welt
| Im innersten zusammenhält,
| Schau alle Würckungskrafft und Saamen
| Und tuh nicht mehr in Worten kramen.
|
| ...


Late version: Faust I (1808)
----------------------------

| NACHT.
| *In einem hochgewölbten, engen, gothischen Zimmer 
  Faust unruhig auf seinem Sessel am Pulte.*

|
| **Faust**
| Habe nun, ach! Philosophie,
| Juristerey und Medicin,
| Und leider auch Theologie!
| Durchaus studirt, mit heißem Bemühn.
| Da steh’ ich nun, ich armer Thor!
| Und bin so klug als wie zuvor;
| Heiße Magister, heiße Doctor gar,
| Und ziehe schon an die zehen Jahr,
| Herauf, herab und quer und krumm,
| Meine Schüler an der Nase herum –
| Und sehe, daß wir nichts wissen können!
| Das will mir schier das Herz verbrennen.
| Zwar bin ich gescheidter als alle die Laffen,
| Doctoren, Magister, Schreiber und Pfaffen;
| Mich plagen keine Scrupel noch Zweifel,
| Fürchte mich weder vor Hölle noch Teufel –
| Dafür ist mir auch alle Freud’ entrissen,
| Bilde mir nicht ein was rechts zu wissen,
| Bilde mir nicht ein, ich könnte was lehren,
| Die Menschen zu bessern und zu bekehren.
| Auch hab’ ich weder Gut noch Geld,
| Noch Ehr’ und Herrlichkeit der Welt.
| Es möchte kein Hund so länger leben!
| Drum hab’ ich mich der Magie ergeben,
| Ob mir durch Geistes Kraft und Mund
| Nicht manch Geheimniß würde kund;
| Daß ich nicht mehr mit sauerm Schweiß,
| Zu sagen brauche, was ich nicht weiß;
| Daß ich erkenne, was die Welt
| Im Innersten zusammenhält,
| Schau’ alle Wirkenskraft und Samen,
| Und thu’ nicht mehr in Worten kramen.
| 
| ...


Diff view Faust I versus Urfaust
--------------------------------

| NACHT.
| *In einem hochgewölbten, engen, gothischen Zimmer*
  :add:`*Faust unruhig auf seinem Sessel am Pulte.*`

|
| **Faust** :del:`*unruhig auf seinem Sessel am Pulten.*`
| Habe nun, ach! :del:`die` Philosophie,

.. change::
    + | Juristerey und Medicin,
    - | Medizin und Juristerey
    
| Und leider auch :del:`die` Theologie!
| Durchaus studirt, mit :change:`heisser Müh-|+heißem Bemühn`.
| Da steh’ ich nun, ich armer Thor!
| Und bin so klug als wie zuvor;

.. change::
    - | Heisse Docktor und Professor gar
    + | Heiße Magister, heiße Doctor gar,
    
| Und ziehe schon an die zehen Jahr,
| Herauf, herab und quer und krumm,
| Meine Schüler an der Nas\ :add:`e` herum –
| Und seh\ :add:`e`, dass wir nichts wissen können\ :change:`:-|+!`
| Das will mir schier das Herz verbrennen.
| Zwar binn ich gescheiter als alle die Laffen
| Docktor\ :change:`s-|+en`, :change:`Professors-|+Magister`, Schreiber 
  und Pfaffen,
| Mich plagen keine Skrupel noch Zweifel,
| Fürcht mich weder vor Höll noch Teufel.
| Dafür ist mir auch all Freud entrissen,
| Bild\ :add:`e` mir nicht ein, was rechts zu wissen,
| Bild\ :add:`e` mir nicht ein, ich könnt\ :add:`e` was lehren
| Die Menschen zu bessern und zu bekehren,
| Auch hab ich weder Gut noch Geld
| Noch Ehr und Herrlichkeit der Welt.
| Es :change:`mögt-|+möchte` kein Hund so länger leben
| Drum hab ich mich der Magie ergeben,
| Ob mir durch Geistes Krafft und Mund
| Nicht manch Geheimnis :change:`werde-|+würde` kund,
| Dass ich nicht mehr mit sau\ :change:`re-|+er`\ m Schweiß

.. change::
    - | Rede von dem, was ich nicht weis,
    + | Zu sagen brauche, was ich nicht weiß;

| Dass ich erkenne, was die Welt
| Im Innersten zusammenhält,
| Schau alle :change:`Würckungskrafft-|+Wirkenskraft` und Samen
| Und thu nicht mehr in Worten kramen.
| 
| ...
| 
| 


.. code-block:: rst

   | NACHT.
   | *In einem hochgewölbten, engen, gothischen Zimmer*
     :add:`*Faust unruhig auf seinem Sessel am Pulte.*`
   
   |
   | **Faust** :del:`*unruhig auf seinem Sessel am Pulten.*`
   | Habe nun, ach! :del`die` Philosophie,
   
   .. change::
       + | Juristerey und Medicin,
       - | Medizin und Juristerey
       
   | Und leider auch :del:`die` Theologie!
   | Durchaus studirt, mit :change:`heisser Müh-|+heißem Bemühn`.
   | Da steh’ ich nun, ich armer Thor!
   | Und bin so klug als wie zuvor;
   
   .. change::
       - | Heisse Docktor und Professor gar
       + | Heiße Magister, heiße Doctor gar,
       
   | Und ziehe schon an die zehen Jahr,
   | Herauf, herab und quer und krumm,
   | Meine Schüler an der Nas\ :add:`e` herum –
   | Und seh\ :add:`e`, dass wir nichts wissen können\ :change:`:-|+!`
   | Das will mir schier das Herz verbrennen.
   | Zwar binn ich gescheiter als alle die Laffen
   | Docktor\ :change:`s-|+en`, :change:`Professors-|+Magister`, Schreiber 
     und Pfaffen,
   | Mich plagen keine Skrupel noch Zweifel,
   | Fürcht mich weder vor Höll noch Teufel.
   | Dafür ist mir auch all Freud entrissen,
   | Bild\ :add:`e` mir nicht ein, was rechts zu wissen,
   | Bild\ :add:`e` mir nicht ein, ich könnt\ :add:`e` was lehren
   | Die Menschen zu bessern und zu bekehren,
   | Auch hab ich weder Gut noch Geld
   | Noch Ehr und Herrlichkeit der Welt.
   | Es :change:`mögt-|+möchte` kein Hund so länger leben
   | Drum hab ich mich der Magie ergeben,
   | Ob mir durch Geistes Krafft und Mund
   | Nicht manch Geheimnis :change:`werde-|+würde` kund,
   | Dass ich nicht mehr mit sau\ :change:`re-|+er`\ m Schweiß
   
   .. change::
       - | Rede von dem, was ich nicht weis,
       + | Zu sagen brauche, was ich nicht weiß;
   
   | Dass ich erkenne, was die Welt
   | Im Innersten zusammenhält,
   | Schau alle :change:`Würckungskrafft-|+Wirkenskraft` und Samen
   | Und thu nicht mehr in Worten kramen.
   | 
   | ...



