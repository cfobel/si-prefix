from libcpp.string cimport string


cdef extern from "src/si_prefix.hpp" namespace 'si_prefix' nogil:
    string format(double value, int precision)
