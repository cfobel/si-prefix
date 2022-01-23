# coding: utf-8
from __future__ import division

import math
import re

from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

# Print a floating-point number in engineering notation.
# Ported from [C version][1] written by
# Jukka “Yucca” Korpela <jkorpela@cs.tut.fi>.
#
# [1]: http://www.cs.tut.fi/~jkorpela/c/eng.html

#: .. versionchanged:: 1.0
#:     Define as unicode string and use µ (i.e., ``\N{MICRO SIGN}``, ``\x0b5``)
#:     to denote micro (not u).
#:
#:     .. seealso::
#:
#:         `Issue #4`_.
#:
#:         `Forum post`_ discussing unicode using µ as an example.
#:
#:         `The International System of Units (SI) report`_ from the Bureau
#:         International des Poids et Mesures
#:
#: .. _`Issue #4`: https://github.com/cfobel/si-prefix/issues/4
#: .. _`Forum post`: https://mail.python.org/pipermail/python-list/2009-February/525913.html
#: .. _`The International System of Units (SI) report`: https://www.bipm.org/utils/common/pdf/si_brochure_8_en.pdf
SI_PREFIX_UNITS = u"yzafpnµm kMGTPEZY"

#: .. versionchanged:: 1.0
#:     Use unicode string for SI unit to support micro (i.e., µ) character.
#:
#:     .. seealso::
#:
#:         `Issue #4`_.
#:
#: .. _`Issue #4`: https://github.com/cfobel/si-prefix/issues/4
CRE_SI_NUMBER = re.compile(r'^\s*(?P<number>(?P<integer>[+\-]?\d+)?'
                           r'(?P<fraction>.\d+)?)\s*'
                           r'(?P<si_unit>[' + SI_PREFIX_UNITS + r'])?\s*$')


def split(value, precision=1):
    """
    Split `value` into value and "exponent-of-10", where "exponent-of-10" is a
    multiple of 3.  This corresponds to SI prefixes.

    Returns tuple, where the second value is the "exponent-of-10" and the first
    value is `value` divided by the "exponent-of-10".

    Args
    ----
    value : int, float
        Input value.
    precision : int
        Number of digits after decimal place to include.

    Returns
    -------
    tuple
        The second value is the "exponent-of-10" and the first value is `value`
        divided by the "exponent-of-10".

    Examples
    --------

    .. code-block:: python

        si_prefix.split(0.04781)   ->  (47.8, -3)
        si_prefix.split(4781.123)  ->  (4.8, 3)

    See :func:`si_format` for more examples.
    """
    negative = False
    digits = precision + 1

    if value < 0.:
        value = -value
        negative = True
    elif value == 0.:
        return 0., 0

    expof10 = int(math.log10(value))
    if expof10 > 0:
        expof10 = (expof10 // 3) * 3
    else:
        expof10 = (-expof10 + 3) // 3 * (-3)

    value *= 10 ** (-expof10)

    if value >= 1000.:
        value /= 1000.0
        expof10 += 3
    elif value >= 100.0:
        digits -= 2
    elif value >= 10.0:
        digits -= 1

    if negative:
        value *= -1

    return value, int(expof10)


def prefix(expof10):
    """
    Args:

        expof10 : Exponent of a power of 10 associated with a SI unit
            character.

    Returns:

        str : One of the characters in "yzafpnum kMGTPEZY".
    """
    prefix_levels = (len(SI_PREFIX_UNITS) - 1) // 2
    si_level = expof10 // 3

    if abs(si_level) > prefix_levels:
        raise ValueError("Exponent out range of available prefixes.")
    return SI_PREFIX_UNITS[si_level + prefix_levels]


def si_format(value, precision=1, format_str=u'{value} {prefix}',
              exp_format_str=u'{value}e{expof10}', trailing_zeroes=False):
    """
    Format value to string with SI prefix, using the specified precision.

    Parameters
    ----------
    value : int, float
        Input value.
    precision : int
        Number of digits after decimal place to include.
    exp_format_str : str or unicode
        Format string where ``{prefix}`` and ``{value}`` represent the SI
        prefix and the value (scaled according to the prefix), respectively.
        The default format matches the `SI prefix style`_ format.
    format_str : str or unicode
        Format string where ``{expof10}`` and ``{value}`` represent the
        exponent of 10 and the value (scaled according to the exponent of 10),
        respectively.  This format is used if the absolute exponent of 10 value
        is greater than 24.
    trailing_zeroes : bool
        Include trailing zeroes if number of decimals in value is less than the precision

    Returns
    -------
    unicode
        :data:`value` formatted according to the `SI prefix style`_.

    Examples
    --------

    For example, with `precision=2`:

    .. code-block:: python

        1e-27 --> 1.00e-27
        1.764e-24 --> 1.76 y
        7.4088e-23 --> 74.09 y
        3.1117e-21 --> 3.11 z
        1.30691e-19 --> 130.69 z
        5.48903e-18 --> 5.49 a
        2.30539e-16 --> 230.54 a
        9.68265e-15 --> 9.68 f
        4.06671e-13 --> 406.67 f
        1.70802e-11 --> 17.08 p
        7.17368e-10 --> 717.37 p
        3.01295e-08 --> 30.13 n
        1.26544e-06 --> 1.27 u
        5.31484e-05 --> 53.15 u
        0.00223223 --> 2.23 m
        0.0937537 --> 93.75 m
        3.93766 --> 3.94
        165.382 --> 165.38
        6946.03 --> 6.95 k
        291733 --> 291.73 k
        1.22528e+07 --> 12.25 M
        5.14617e+08 --> 514.62 M
        2.16139e+10 --> 21.61 G
        9.07785e+11 --> 907.78 G
        3.8127e+13 --> 38.13 T
        1.60133e+15 --> 1.60 P
        6.7256e+16 --> 67.26 P
        2.82475e+18 --> 2.82 E
        1.1864e+20 --> 118.64 E
        4.98286e+21 --> 4.98 Z
        2.0928e+23 --> 209.28 Z
        8.78977e+24 --> 8.79 Y
        3.6917e+26 --> 369.17 Y
        1.55051e+28 --> 15.51e+27
        6.51216e+29 --> 651.22e+27

    .. versionchanged:: 1.0
        Use unicode string for :data:`format_str` and SI value format string to
        support micro (i.e., µ) characte, and change return type to unicode
        string.

        .. seealso::

            `Issue #4`_.

    .. _`Issue #4`: https://github.com/cfobel/si-prefix/issues/4
    .. _SI prefix style:
        https://physics.nist.gov/cuu/Units/checklist.html
    """
    svalue, expof10 = split(value, precision)
    if trailing_zeroes:
        value_str = f"{svalue:.{precision}f}"
    else:
        # rounds to precision without trailing zeroes which drives me insane
        value_str = f"{round(svalue, precision):g}"
    try:
        return format_str.format(value=value_str,
                                 prefix=prefix(expof10).strip()).strip()
    except ValueError:
        sign = ''
        if expof10 > 0:
            sign = "+"
        return exp_format_str.format(value=value_str,
                                     expof10=''.join([sign, str(expof10)])).strip()


def si_parse(value):
    """
    Parse a value expressed using SI prefix units to a floating point number.

    Parameters
    ----------
    value : str or unicode
        Value expressed using SI prefix units (as returned by :func:`si_format`
        function).


    .. versionchanged:: 1.0
        Use unicode string for SI unit to support micro (i.e., µ) character.

        .. seealso::

            `Issue #4`_.

    .. _`Issue #4`: https://github.com/cfobel/si-prefix/issues/4
    """
    CRE_10E_NUMBER = re.compile(r'^\s*(?P<integer>[+\-]?\d+)?'
                                r'(?P<fraction>.\d+)?\s*([eE]\s*'
                                r'(?P<expof10>[+\-]?\d+))?$')

    match = CRE_10E_NUMBER.match(value)
    if match:
        # Can be parse using `float`.
        assert (match.group('integer') is not None or
                match.group('fraction') is not None)
        return float(value)
    match = CRE_SI_NUMBER.match(value)
    assert (match.group('integer') is not None or
            match.group('fraction') is not None)
    d = match.groupdict()
    si_unit = d['si_unit'] if d['si_unit'] else ' '
    prefix_levels = (len(SI_PREFIX_UNITS) - 1) // 2
    scale = 10 ** (3 * (SI_PREFIX_UNITS.index(si_unit) - prefix_levels))
    return float(d['number']) * scale


def si_prefix_scale(si_unit):
    """
    Parameters
    ----------
    si_unit : str
        SI unit character, i.e., one of "yzafpnµm kMGTPEZY".

    Returns
    -------
    int
        Multiple associated with `si_unit`, e.g., 1000 for `si_unit=k`.
    """
    return 10 ** si_prefix_expof10(si_unit)


def si_prefix_expof10(si_unit):
    """
    Parameters
    ----------
    si_unit : str
        SI unit character, i.e., one of "yzafpnµm kMGTPEZY".

    Returns
    -------
    int
        Exponent of the power of ten associated with `si_unit`, e.g., 3 for
        `si_unit=k` and -6 for `si_unit=µ`.
    """
    prefix_levels = (len(SI_PREFIX_UNITS) - 1) // 2
    return 3 * (SI_PREFIX_UNITS.index(si_unit) - prefix_levels)
