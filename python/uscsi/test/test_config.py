from __future__ import print_function

import unittest

from numpy import asarray
from numpy.testing import assert_array_almost_equal as assert_array_equal
from numpy.testing import assert_equal

from .._internal import (GLPSPrinter as dictshow, _GLPSParse)

class GLPSParser(object):
    def parse(self, s):
        return _GLPSParse(s)


class testParse(unittest.TestCase):
    maxDiff = 1000

    def test_fail(self):
        P = GLPSParser()
        self.assertRaisesRegexp(RuntimeError, ".*invalid charactor.*",
                                P.parse, b"\xff\xfe")

        self.assertRaisesRegexp(RuntimeError, "No beamlines defined by this file",
                                P.parse, "")

        self.assertRaisesRegexp(RuntimeError, "No beamlines defined by this file",
                                P.parse, "A = 3;")

        self.assertRaisesRegexp(RuntimeError, "syntax error",
                                P.parse, "A = =;")

        self.assertRaisesRegexp(RuntimeError, ".*referenced before definition",
                                P.parse, "A = A;")

        self.assertRaisesRegexp(RuntimeError, ".*referenced before definition",
                                P.parse, "A = B;")

        self.assertRaisesRegexp(RuntimeError, "syntax error",
                                P.parse, "A = [;")

        self.assertRaisesRegexp(RuntimeError, "syntax error",
                                P.parse, "A = [ 1, 2;")

        self.assertRaisesRegexp(RuntimeError, "syntax error",
                                P.parse, "A = [ 1, 2, ;")

        self.assertRaisesRegexp(RuntimeError, ".*Vector element types must be scalar not type.*",
                                P.parse, "A = [ 1, \"bar\", ;")

        self.assertRaisesRegexp(RuntimeError, ".*Unterminated quote",
                                P.parse, "A = \"oops ...")

        self.assertRaisesRegexp(RuntimeError, "syntax error",
                                P.parse, "A: line = (")

        self.assertRaisesRegexp(RuntimeError, ".*invalid.*referenced before definition",
                                P.parse, "A: line = ( invalid")

        self.assertRaisesRegexp(RuntimeError, ".*invalid.*referenced before definition",
                                P.parse, "bar: foo; A: line = ( bar, invalid")

        self.assertRaisesRegexp(RuntimeError, "syntax error",
                                P.parse, "bar:: foo;")

        self.assertRaisesRegexp(RuntimeError, "syntax error",
                                P.parse, "bar: : foo;")

        self.assertRaisesRegexp(RuntimeError, "syntax error",
                                P.parse, ":bar : foo;")
    def test_calc_err(self):
        P = GLPSParser()
        self.assertRaisesRegexp(RuntimeError, ".*division results in non-finite value",
                                P.parse, "foo = 4/0;")
    def test_utf8(self):
        "Can pass any 1-255 in quoted string"
        P = GLPSParser()

        C = P.parse("""
hello = "test\x1f";
x1: drift, L=4; # comments are ignored
foo: LINE = (x1, x1);
""")
        
        self.assertEqual(C, {
            'hello':"test\x1f",
            'name':'foo',
            'elements':[
                {'name':'x1', 'type':'drift', 'L':4.0},
                {'name':'x1', 'type':'drift', 'L':4.0},
            ],
        })

    def test_good(self):
        P = GLPSParser()

        C = P.parse("""
hello = 42;
x1: drift, L=4;
foo: LINE = (x1, x1);
""")

        self.assertEqual(C, {
            'hello':42.0,
            'name':'foo',
            'elements':[
                {'name':'x1', 'type':'drift', 'L':4.0},
                {'name':'x1', 'type':'drift', 'L':4.0},
            ],
        })

    def test_good2(self):
        P = GLPSParser()

        C = P.parse("""
hello = 42;
x1: drift, L=4;
x:2: quad, L=1;
f:oo: LINE = (2*x1, x:2);
""")

        self.assertEqual(C, {
            'hello':42.0,
            'name':'f:oo',
            'elements':[
                {'name':'x1', 'type':'drift', 'L':4.0},
                {'name':'x1', 'type':'drift', 'L':4.0},
                {'name':'x:2', 'type':'quad', 'L':1.0},
            ],
        })

    def test_good3(self):
        P = GLPSParser()

        C = P.parse("""
hello = 42;
S: source;
x1: drift, L=4;
x2: quad, L=1;
foo: LINE = (S, 2*x1, x2);
""")

        E = {
            'hello':42.0,
            'name':'foo',
            'elements':[
                {'name':'S', 'type':'source'},
                {'name':'x1', 'type':'drift', 'L':4.0},
                {'name':'x1', 'type':'drift', 'L':4.0},
                {'name':'x2', 'type':'quad', 'L':1.0},
            ],
        }
        try:
            self.assertEqual(C, E)
        except:
            from pprint import pformat
            print('Actual', pformat(C))
            print('Expect', pformat(E))
            raise

    def test_calc(self):
        P = GLPSParser()

        C = P.parse("""
hello = 4*10--2;
x1: drift, L=4;
foo: LINE = (0*x1, (3-1)*x1);
""")

        self.assertEqual(C, {
            'hello':42.0,
            'name':'foo',
            'elements':[
                {'name':'x1', 'type':'drift', 'L':4.0},
                {'name':'x1', 'type':'drift', 'L':4.0},
            ],
        })

    def test_arr(self):
        P = GLPSParser()
        C = P.parse("""
hello = [1,2, 3, 4];
x1: drift, L=4, extra = [1, 3, 5];
foo: LINE = (x1, x1);
""")

        assert_array_equal(C['hello'], asarray([1,2,3,4]))
        assert_array_equal(C['elements'][0]['extra'], asarray([1,3,5]))
