# distutils: language = c++
from si_prefix.si_prefix cimport format as _format


def si_format(double value, int precision=1):
    return _format(value, precision)
