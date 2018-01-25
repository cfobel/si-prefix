# coding: utf-8
from nose.tools import eq_
from si_prefix import si_format


#: .. versionchanged:: 1.0
#:     Use unicode strings and use µ to denote micro (not u).
TEST_CASES = [(1e-27, u'1.00e-27'),
              (1.764e-24, u'1.76 y'),
              (7.4088e-23, u'74.09 y'),
              (3.1117e-21, u'3.11 z'),
              (1.30691e-19, u'130.69 z'),
              (5.48903e-18, u'5.49 a'),
              (2.30539e-16, u'230.54 a'),
              (9.68265e-15, u'9.68 f'),
              (4.06671e-13, u'406.67 f'),
              (1.70802e-11, u'17.08 p'),
              (7.17368e-10, u'717.37 p'),
              (3.01295e-08, u'30.13 n'),
              (1.26544e-06, u'1.27 µ'),
              (5.31484e-05, u'53.15 µ'),
              (0.00223223, u'2.23 m'),
              (0.0937537, u'93.75 m'),
              (3.93766, u'3.94 '),  # Space added to help alignment
              (165.382, u'165.38 '),  # Space added to help alignment
              (6946.03, u'6.95 k'),
              (291733, u'291.73 k'),
              (1.22528e+07, u'12.25 M'),
              (5.14617e+08, u'514.62 M'),
              (2.16139e+10, u'21.61 G'),
              (3.8127e+13, u'38.13 T'),
              (1.60133e+15, u'1.60 P'),
              (6.7256e+16, u'67.26 P'),
              (2.82475e+18, u'2.82 E'),
              (1.1864e+20, u'118.64 E'),
              (4.98286e+21, u'4.98 Z'),
              (2.0928e+23, u'209.28 Z'),
              (8.78977e+24, u'8.79 Y'),
              (3.6917e+26, u'369.17 Y'),
              (1.55051e+28, u'15.51e+27'),
              (6.51216e+29, u'651.22e+27')]


#: .. versionchanged:: 1.0
#:    Yield each individual test.
def test_si_format():
    for value, result in TEST_CASES:
        # Test that pure Python format function matches expected output.
        yield _test_si_format, value, result


def _test_si_format(value, result):
    '''
    .. versionadded:: 1.0
    '''
    eq_(si_format(value, 2), result)
