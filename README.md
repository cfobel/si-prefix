# si_prefix #

Functions for formatting numbers according to SI standards.

Example usage:

    from si_prefix import si_format

    print si_format(.5)
    # 500.0m  (default precision is 1)

    print si_format(.01331, precision=2)
    # 13.31m

    print si_format(1331, precision=2)
    # 1.33k

    print si_format(1331, precision=0)
    # 1k


# Credits #

Ported from [C version][1] written by
Jukka “Yucca” Korpela <jkorpela@cs.tut.fi>.

[1]: http://www.cs.tut.fi/~jkorpela/c/eng.html
