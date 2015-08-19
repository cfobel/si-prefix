# coding: utf-8
from nose.tools import eq_
from si_prefix import si_format as c_si_format
from si_prefix._si_prefix import si_format


TEST_CASES = [(1e-27, '1.00e-27'),
              (1.764e-24, '1.76y'),
              (7.4088e-23, '74.09y'),
              (3.1117e-21, '3.11z'),
              (1.30691e-19, '130.69z'),
              (5.48903e-18, '5.49a'),
              (2.30539e-16, '230.54a'),
              (9.68265e-15, '9.68f'),
              (4.06671e-13, '406.67f'),
              (1.70802e-11, '17.08p'),
              (7.17368e-10, '717.37p'),
              (3.01295e-08, '30.13n'),
              (1.26544e-06, '1.27u'),
              (5.31484e-05, '53.15u'),
              (0.00223223, '2.23m'),
              (0.0937537, '93.75m'),
              (3.93766, '3.94 '),  # Space added to help alignment
              (165.382, '165.38 '),  # Space added to help alignment
              (6946.03, '6.95k'),
              (291733, '291.73k'),
              (1.22528e+07, '12.25M'),
              (5.14617e+08, '514.62M'),
              (2.16139e+10, '21.61G'),
              (3.8127e+13, '38.13T'),
              (1.60133e+15, '1.60P'),
              (6.7256e+16, '67.26P'),
              (2.82475e+18, '2.82E'),
              (1.1864e+20, '118.64E'),
              (4.98286e+21, '4.98Z'),
              (2.0928e+23, '209.28Z'),
              (8.78977e+24, '8.79Y'),
              (3.6917e+26, '369.17Y'),
              (1.55051e+28, '15.51e+27'),
              (6.51216e+29, '651.22e+27')]


def test_si_format():
    for value, result in TEST_CASES:
        # Test that pure Python format function matches expected output.
        eq_(si_format(value, 2), result)
        # Test that Cython wrapped C++ format function matches expected output.
        eq_(c_si_format(value, 2), result)
        for i in xrange(4):
            # Test that Cython wrapped C++ function matches pure Python
            # function for several precisions.
            eq_(si_format(value, i), c_si_format(value, i))
