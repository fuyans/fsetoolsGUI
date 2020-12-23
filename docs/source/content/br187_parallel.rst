.. _test_label:

BR 187 parallel oriented rectangle emitter and receiver
-------------------------------------------------------

Quality management
~~~~~~~~~~~~~~~~~~

+------------+--------+---------+----------------------------------------------+
| Date       | Author | Checker | Remarks                                      |
+============+========+=========+==============================================+
| 2020/03/11 | Ian F. | Alex T. | Initial, receiver within emitter plane       |
+------------+--------+---------+----------------------------------------------+
| 2020/03/27 | Ian F. | Zak A.  | Receiver within and outside of emitter plane |
+------------+--------+---------+----------------------------------------------+

Theoretical model
~~~~~~~~~~~~~~~~~

To calculate the radiation intensity at points which are not ealigned with the centre of the source or to consider mor ecomplex shapes for the radiating surface, the calculation of a view factor for a point aligned with the corner of a rectangular source.

The view factor for a rectangule as seen from the corner can be found from:

.. math::
   \phi = \frac{1}{2\pi}\left(\frac{X}{\sqrt{1+X^2}}\tan^{-1}{\left(\frac{Y}{\sqrt{1+X^2}} \right )}+\frac{Y}{\sqrt{1+Y}}\tan^{-1}{\left(\frac{X}{\sqrt{1+Y^2}} \right )}\right)

Where :math:`X=\frac{W}{2s}` and :math:`Y=\frac{H}{2s}`.

In order to calculate the imposed heat flux from an emitter at any given point on the emitter plan (and at a distance :math:`S`), the following scenarios are considered.

Within the emitter rectangle
::::::::::::::::::::::::::::

todo, test custom link :ref:`link<test_label>`.

Outside of the emitter rectangle
::::::::::::::::::::::::::::::::

todo

Referenced original texts in BR 187
:::::::::::::::::::::::::::::::::::

.. figure:: content/br187.assets/p34.png
    :width: 100%
    :alt: page 34
