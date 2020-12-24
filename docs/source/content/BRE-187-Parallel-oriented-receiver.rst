BR 187 Parallel oriented receiver
---------------------------------

.. list-table::
    :widths: 15 15 15 55
    :header-rows: 1

    * - Date
      - Author
      - Checker
      - Remarks
    * - 2020/03/11
      - Ian F.
      - Alex T.
      - Initial, parallel orientation receiver within emitter plane
    * - 2020/03/27
      - \-
      - Zak A.
      - Parallel orientation, receiver within and outside of emitter plane

View factor
~~~~~~~~~~~

Parallel oriented emitter and receiver
::::::::::::::::::::::::::::::::::::::

.. math::
   \phi = \frac{1}{2\pi}\left(\frac{X}{\sqrt{1+X^2}}\tan^{-1}{\left(\frac{Y}{\sqrt{1+X^2}} \right )}+\frac{Y}{\sqrt{1+Y^2}}\tan^{-1}{\left(\frac{X}{\sqrt{1+Y^2}} \right )}\right)

Where :math:`X=\frac{W}{S}` and :math:`Y=\frac{H}{S}`.

Perpendicular oriented emitter and receiver
::::::::::::::::::::::::::::::::::::::

.. math::
   \phi=\frac{1}{2\pi}\left(\tan^{-1}\left({X} \right )-\frac{1}{\sqrt{Y^2+1}}\tan^{-1}\left(\frac{X}{\sqrt{Y^2+1}} \right ) \right )

Where :math:`X=\frac{W}{S}` and :math:`Y=\frac{H}{S}`.

View factors at any given point on an emitter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Within the emitter rectangle
::::::::::::::::::::::::::::

todo

Outside of the emitter rectangle
::::::::::::::::::::::::::::::::

todo

Referenced original texts in BR 187
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: BRE-187/p33.svg
    :width: 100%
    :alt: BR 187, Page 33

.. figure:: BRE-187/p34.svg
    :width: 100%
    :alt: BR 187, Page 34

.. figure:: BRE-187/p35.svg
    :width: 100%
    :alt: BR 187, Page 35

.. figure:: BRE-187/p36.svg
    :width: 100%
    :alt: BR 187, Page 36
