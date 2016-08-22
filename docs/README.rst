si\_prefix
==========

Functions for formatting numbers according to SI standards.

Example usage:

::

    from si_prefix import si_format

    print si_format(.5)
    # 500.0 m  (default precision is 1)

    print si_format(.01331, precision=2)
    # 13.31 m

    print si_format(1331, precision=2)
    # 1.33 k

    print si_format(1331, precision=0)
    # 1 k

Credits
=======

Written by Christian Fobel christian@fobel.net

Ported from `C version <http://www.cs.tut.fi/~jkorpela/c/eng.html>`__
written by Jukka “Yucca” Korpela jkorpela@cs.tut.fi.
