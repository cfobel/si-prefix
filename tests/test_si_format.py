# coding: utf-8
import pytest
from si_prefix import si_format, si_parse, si_prefix_expof10, si_prefix_scale

SI_FORMAT_TEST_CASES = [
    (1e-27, "1.00e-27"),
    (1.764e-24, "1.76 y"),
    (7.4088e-23, "74.09 y"),
    (3.1117e-21, "3.11 z"),
    (1.30691e-19, "130.69 z"),
    (5.48903e-18, "5.49 a"),
    (2.30539e-16, "230.54 a"),
    (9.68265e-15, "9.68 f"),
    (4.06671e-13, "406.67 f"),
    (1.70802e-11, "17.08 p"),
    (7.17368e-10, "717.37 p"),
    (3.01295e-08, "30.13 n"),
    (1.26544e-06, "1.27 µ"),
    (5.31484e-05, "53.15 µ"),
    (0.00223223, "2.23 m"),
    (0.0937537, "93.75 m"),
    (3.93766, "3.94 "),  # Space added to help alignment
    (165.382, "165.38 "),  # Space added to help alignment
    (6946.03, "6.95 k"),
    (291733, "291.73 k"),
    (1.22528e07, "12.25 M"),
    (5.14617e08, "514.62 M"),
    (2.16139e10, "21.61 G"),
    (3.8127e13, "38.13 T"),
    (1.60133e15, "1.60 P"),
    (6.7256e16, "67.26 P"),
    (2.82475e18, "2.82 E"),
    (1.1864e20, "118.64 E"),
    (4.98286e21, "4.98 Z"),
    (2.0928e23, "209.28 Z"),
    (8.78977e24, "8.79 Y"),
    (3.6917e26, "369.17 Y"),
    (1.55051e28, "15.51e+27"),
    (6.51216e29, "651.22e+27"),
    (0, "0.00 "),
    (-1.234, "-1.23 "),
]
"""
.. versionchanged:: 1.0
    Use unicode strings and use µ to denote micro (not u).
"""

SI_PARSE_TEST_CASES = [
    ("1.00e-27", 1e-27),
    ("1.76 y", 1.764e-24),
    ("74.09 y", 7.4088e-23),
    ("3.11 z", 3.1117e-21),
    ("130.69 z", 1.30691e-19),
    ("5.49 a", 5.48903e-18),
    ("230.54 a", 2.30539e-16),
    ("9.68 f", 9.68265e-15),
    ("406.67 f", 4.06671e-13),
    ("17.08 p", 1.70802e-11),
    ("717.37 p", 7.17368e-10),
    ("30.13 n", 3.01295e-08),
    ("1.27 µ", 1.26544e-06),
    ("53.15 µ", 5.31484e-05),
    ("2.23 m", 0.00223223),
    ("93.75 m", 0.0937537),
    ("3.94 ", 3.93766),
    ("165.38 ", 165.382),
    ("6.95 k", 6946.03),
    ("291.73 k", 291733),
    ("12.25 M", 1.22528e07),
    ("514.62 M", 5.14617e08),
    ("21.61 G", 2.16139e10),
    ("38.13 T", 3.8127e13),
    ("1.60 P", 1.60133e15),
    ("67.26 P", 6.7256e16),
    ("2.82 E", 2.82475e18),
    ("118.64 E", 1.1864e20),
    ("4.98 Z", 4.98286e21),
    ("209.28 Z", 2.0928e23),
    ("8.79 Y", 8.78977e24),
    ("369.17 Y", 3.6917e26),
    ("15.51e+27", 1.55051e28),
    ("651.22e+27", 6.51216e29),
]

SI_PREFIX_SCALE_TEST_CASES = [
    ("y", 1e-24),
    ("z", 1e-21),
    ("a", 1e-18),
    ("f", 1e-15),
    ("p", 1e-12),
    ("n", 1e-9),
    ("µ", 1e-6),
    ("m", 1e-3),
    (" ", 1e0),
    ("k", 1e3),
    ("M", 1e6),
    ("G", 1e9),
    ("T", 1e12),
    ("P", 1e15),
    ("E", 1e18),
    ("Z", 1e21),
    ("Y", 1e24),
]

SI_PREFIX_EXPOF10_TEST_CASES = [
    ("y", -24),
    ("z", -21),
    ("a", -18),
    ("f", -15),
    ("p", -12),
    ("n", -9),
    ("µ", -6),
    ("m", -3),
    (" ", 0),
    ("k", 3),
    ("M", 6),
    ("G", 9),
    ("T", 12),
    ("P", 15),
    ("E", 18),
    ("Z", 21),
    ("Y", 24),
]


@pytest.mark.parametrize("value, result", SI_FORMAT_TEST_CASES)
def test_si_format(value, result):
    assert si_format(value, 2) == result


@pytest.mark.parametrize("value, result", SI_PARSE_TEST_CASES)
def test_si_parse(value, result):
    assert si_parse(value) == pytest.approx(result, rel=1e-2)


@pytest.mark.parametrize("si_unit, scale", SI_PREFIX_SCALE_TEST_CASES)
def test_si_prefix_scale(si_unit, scale):
    assert si_prefix_scale(si_unit) == pytest.approx(scale, rel=1e-2)


@pytest.mark.parametrize("si_unit, expof10", SI_PREFIX_EXPOF10_TEST_CASES)
def test_si_prefix_expof10(si_unit, expof10):
    assert si_prefix_expof10(si_unit) == expof10
