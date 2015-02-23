#ifndef ___SI_PREFIX__HPP___
#define ___SI_PREFIX__HPP___

/* Print a floating-point number in engineering notation */
/* Documentation: http://www.cs.tut.fi/~jkorpela/c/eng.html */

/* Smallest power of ten for which there is a prefix defined.
   If the set of prefixes will be extended, change this constant
   and update the table "prefix". */
#include <stdexcept>
#include <string>
#include <sstream>
#include <utility>
#include <stdio.h>
#include <cmath>


namespace si_prefix {
  inline std::pair<double, int> split(double value, int precision=1) {
    /* Split `value` into value and "exponent-of-10", where "exponent-of-10" is
     * a multiple of 3.  This corresponds to SI prefixes.
     *
     * Returns `std::pair`, where the second value is the "exponent-of-10" and
     * the first value is `value` divided by the "exponent-of-10".
     *
     * For example:
     *
     *     si_prefix::split(0.04781)   ->  (47.8, -3)
     *     si_prefix::split(4781.123)  ->  (4.8, 3)
     *
     * See `si_prefix::format` for more examples. */
    int expof10;
    bool negative = false;
    int digits = precision + 1;

    if (value < 0.) {
      value = -value;
      negative = true;
    } else if (value == 0.) {
      return std::make_pair(0, 0);
    }

    expof10 = static_cast<int>(log10(value));
    if(expof10 > 0) {
      expof10 = (expof10 / 3) * 3;
    } else {
      expof10 = (-expof10 + 3) / 3 * (-3);
    }

    value *= pow(10, -expof10);

    if (value >= 1000.) {
      value /= 1000.0;
      expof10 += 3;
    } else if(value >= 100.0) {
      digits -= 2;
    } else if(value >= 10.0) {
      digits -= 1;
    }

    if (negative) {
      value *= -1;
    }

    return std::make_pair(value, expof10);
  }

  inline char prefix(int expof10) {
    std::string prefix("yzafpnum kMGTPEZY");
    const int prefix_levels = (prefix.size() - 1) / 2;
    int si_level = expof10 / 3;

    if (std::abs(static_cast<double>(si_level)) > prefix_levels) {
      throw std::runtime_error("Exponent out range of available prefixes.");
    }
    return prefix.c_str()[si_level + prefix_levels];
  }

  inline std::string format(double value, int precision=1) {
    /* Format value to string with SI prefix, using the specified precision.
     *
     * For example, with `precision=2`:
     *
     *     1e-27 --> 1.00e-27
     *     1.764e-24 --> 1.76 y
     *     7.4088e-23 --> 74.09 y
     *     3.1117e-21 --> 3.11 z
     *     1.30691e-19 --> 130.69 z
     *     5.48903e-18 --> 5.49 a
     *     2.30539e-16 --> 230.54 a
     *     9.68265e-15 --> 9.68 f
     *     4.06671e-13 --> 406.67 f
     *     1.70802e-11 --> 17.08 p
     *     7.17368e-10 --> 717.37 p
     *     3.01295e-08 --> 30.13 n
     *     1.26544e-06 --> 1.27 u
     *     5.31484e-05 --> 53.15 u
     *     0.00223223 --> 2.23 m
     *     0.0937537 --> 93.75 m
     *     3.93766 --> 3.94
     *     165.382 --> 165.38
     *     6946.03 --> 6.95 k
     *     291733 --> 291.73 k
     *     1.22528e+07 --> 12.25 M
     *     5.14617e+08 --> 514.62 M
     *     2.16139e+10 --> 21.61 G
     *     9.07785e+11 --> 907.78 G
     *     3.8127e+13 --> 38.13 T
     *     1.60133e+15 --> 1.60 P
     *     6.7256e+16 --> 67.26 P
     *     2.82475e+18 --> 2.82 E
     *     1.1864e+20 --> 118.64 E
     *     4.98286e+21 --> 4.98 Z
     *     2.0928e+23 --> 209.28 Z
     *     8.78977e+24 --> 8.79 Y
     *     3.6917e+26 --> 369.17 Y
     *     1.55051e+28 --> 15.51e+27
     *     6.51216e+29 --> 651.22e+27 */
    std::pair<double, int> w_si = si_prefix::split(value, precision);
    std::stringstream s;
    s.precision(precision);
    s.setf(std::ios::fixed, std:: ios::floatfield);

    try {
      s << w_si.first << si_prefix::prefix(w_si.second);
    } catch(...) {
      std::string sign;
      if (w_si.second > 0) { sign = "+"; }
      s << w_si.first << "e" << sign << w_si.second;
    }
    return s.str();
};

}

#endif  // #ifndef ___SI_PREFIX__HPP___
