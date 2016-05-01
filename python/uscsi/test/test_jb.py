
import sys
import unittest
import math
import numpy
from numpy import testing as NT
#from numpy.testing import assert_array_almost_equal_nulp as assert_aequal
from numpy.testing import assert_array_almost_equal as assert_aequal

from .. import Machine

from .._internal import (GLPSPrinter as dictshow, _GLPSParse)

import os
datadir = os.path.dirname(__file__)

def print_state(S):
  n = 7
  for i in range(n):
    sys.stdout.write('[')
    for j in range(n):
      sys.stdout.write('%15.8e' % (S.state[i, j]))
      if j != n-1: sys.stdout.write(', ')
    if i != n-1:
      sys.stdout.write('],\n')
    else:
      sys.stdout.write(']\n')

class GLPSParser(object):
    def parse(self, s):
        return _GLPSParse(s)

class testBasic(unittest.TestCase):
  def setUp(self):
    # Called before each test.

   return

  def test_generic(self):
    "Propagate a state matrix through a generic section"

    T = self.expect = numpy.asfarray([
      [1, 0, 0, 0, 0, 0, 0],
      [0, 1, 0, 0, 0, 0, 0],
      [0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0, 1, 0],
      [0, 0, 0, 0, 0, 0, 1]
    ])

    self.M = Machine({
      'sim_type':'MomentMatrix',
      'elements':[
        {'name':'elem0', 'type':'source', 'initial':T},
        {'name':'elem1', 'type':'generic', 'transfer':numpy.identity(7)}
      ]
    })

    S = self.M.allocState({})

    self.M.propagate(S)

    assert_aequal(S.state, [
      [1, 0, 0, 0, 0, 0, 0],
      [0, 1, 0, 0, 0, 0, 0],
      [0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0, 1, 0],
      [0, 0, 0, 0, 0, 0, 1]
    ])

  def test_drift(self):
    "Propagate a state matrix through a drift"

    T = self.expect = numpy.asfarray([
      [0.1, 0,   0,   0,   0,   0,   0],
      [0,   0.2, 0,   0,   0,   0,   0],
      [0,   0,   0.3, 0,   0,   0,   0],
      [0,   0,   0,   0.4, 0,   0,   0],
      [0,   0,   0,   0,   0.5, 0,   0],
      [0,   0,   0,   0,   0,   0.6, 0],
      [0,   0,   0,   0,   0,   0,   0]
    ])

    self.M = Machine({
      'sim_type':'MomentMatrix',
      'elements':[
        {'name':'elem0', 'type':'source', 'initial':T},
        {'name':'elem1', 'type':'drift', 'L':1.234},
      ]
    })

    S = self.M.allocState({})

    self.M.propagate(S)

    assert_aequal(S.state, [
      [ 3.045513e+05,  2.468000e+02,  0.000000e+00,  0.000000e+00,  0.000000e+00,  0.000000e+00, 0],
      [ 2.468000e+02,  2.000000e-01,  0.000000e+00,  0.000000e+00,  0.000000e+00,  0.000000e+00, 0],
      [ 0.000000e+00,  0.000000e+00,  6.091027e+05,  4.936000e+02,  0.000000e+00,  0.000000e+00, 0],
      [ 0.000000e+00,  0.000000e+00,  4.936000e+02,  4.000000e-01,  0.000000e+00,  0.000000e+00, 0],
      [ 0.000000e+00,  0.000000e+00,  0.000000e+00,  0.000000e+00,  5.000000e-01,  0.000000e+00, 0],
      [ 0.000000e+00,  0.000000e+00,  0.000000e+00,  0.000000e+00,  0.000000e+00,  6.000000e-01, 0],
      [ 0,             0,             0,             0,             0,             0,            0]
      ])

  def test_sbend1(self):
    "Propagate a state matrix through a focusing sector bend"

    T = self.expect = numpy.asfarray([
      [0.1, 0,   0,   0,   0,   0,   0],
      [0,   0.2, 0,   0,   0,   0,   0],
      [0,   0,   0.3, 0,   0,   0,   0],
      [0,   0,   0,   0.4, 0,   0,   0],
      [0,   0,   0,   0,   0.5, 0,   0],
      [0,   0,   0,   0,   0,   0.6, 0],
      [0,   0,   0,   0,   0,   0,   0]
    ])

    self.M = Machine({
      'sim_type':'MomentMatrix',
      'elements':[
        {'name':'elem0', 'type':'source', 'initial':T},
        {'name':'elem1', 'type':'sbend', 'L':2.0e-3, 'phi':math.radians(25.0),
         'K':1.0e6},
      ]
    })

    S = self.M.allocState({})

    self.M.propagate(S)

    assert_aequal(S.state, [
       [ 1.71805650e-01, -3.79121906e-02,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0],
       [-3.79121906e-02,  1.24776654e-01,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0],
       [ 0.00000000e+00,  0.00000000e+00,  9.50788149e+00,  9.55147102e+00,  0.00000000e+00,  0.00000000e+00, 0],
       [ 0.00000000e+00,  0.00000000e+00,  9.55147102e+00,  9.60788149e+00,  0.00000000e+00,  0.00000000e+00, 0],
       [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  5.00000000e-01,  0.00000000e+00, 0],
       [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  6.00000000e-01, 0],
       [ 0,               0,               0,               0,               0,               0,              0]
    ], decimal=6)

  def test_sbend2(self):
    "Propagate a state matrix through a defocusing sector bend"

    T = self.expect = numpy.asfarray([
      [0.1, 0,   0,   0,   0,   0,   0],
      [0,   0.2, 0,   0,   0,   0,   0],
      [0,   0,   0.3, 0,   0,   0,   0],
      [0,   0,   0,   0.4, 0,   0,   0],
      [0,   0,   0,   0,   0.5, 0,   0],
      [0,   0,   0,   0,   0,   0.6, 0],
      [0,   0,   0,   0,   0,   0,   0]
    ])

    self.M = Machine({
      'sim_type':'MomentMatrix',
      'elements':[
        {'name':'elem0', 'type':'source', 'initial':T},
        {'name':'elem1', 'type':'sbend', 'L':2.0e-3, 'phi':math.radians(25.0),
         'K':-1.0e6},
      ]
    })

    S = self.M.allocState({})

    self.M.propagate(S)

    assert_aequal(S.state, [
      [ 3.78918063e+00,  3.74852747e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0],
      [ 3.74852747e+00,  3.71358865e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00,  3.82682181e-01, -3.78401248e-02,  0.00000000e+00,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00, -3.78401248e-02,  3.17317819e-01,  0.00000000e+00,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  5.00000000e-01,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  6.00000000e-01, 0],
      [ 0,               0,               0,               0,               0,               0,              0]
    ], decimal=6)

  def test_quad1(self):
    "Propagate a state matrix through a focusing quadrupole"

    T = self.expect = numpy.asfarray([
      [0.1, 0,   0,   0,   0,   0,   0],
      [0,   0.2, 0,   0,   0,   0,   0],
      [0,   0,   0.3, 0,   0,   0,   0],
      [0,   0,   0,   0.4, 0,   0,   0],
      [0,   0,   0,   0,   0.5, 0,   0],
      [0,   0,   0,   0,   0,   0.6, 0],
      [0,   0,   0,   0,   0,   0,   0]
    ])

    self.M = Machine({
      'sim_type':'MomentMatrix',
      'elements':[
        {'name':'elem0', 'type':'source', 'initial':T},
        {'name':'elem1', 'type':'quadrupole', 'L':2.0e-3, 'K':1.1e6, 'B2':0.0},
      ]
    })

    S = self.M.allocState({})

    self.M.propagate(S)

    assert_aequal(S.state, [
      [ 1.61134871e-01, -3.72950224e-02,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0],
      [-3.72950224e-02,  1.32751642e-01,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00,  1.09819606e+01,  1.15461050e+01,  0.00000000e+00,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00,  1.15461050e+01,  1.21501566e+01,  0.00000000e+00,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  5.00000000e-01,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  6.00000000e-01, 0],
      [ 0,               0,               0,               0,               0,               0,              0]
    ], decimal=6)

  def test_quad2(self):
    "Propagate a state matrix through a defocusing quadrupole"

    T = self.expect = numpy.asfarray([
      [0.1, 0,   0,   0,   0,   0,   0],
      [0,   0.2, 0,   0,   0,   0,   0],
      [0,   0,   0.3, 0,   0,   0,   0],
      [0,   0,   0,   0.4, 0,   0,   0],
      [0,   0,   0,   0,   0.5, 0,   0],
      [0,   0,   0,   0,   0,   0.6, 0],
      [0,   0,   0,   0,   0,   0,   0]
    ])

    self.M = Machine({
      'sim_type':'MomentMatrix',
      'elements':[
        {'name':'elem0', 'type':'source', 'initial':T},
        {'name':'elem1', 'type':'quadrupole', 'L':2.0e-3, 'K':-1.1e6, 'B2':0.0},
      ]
    })

    S = self.M.allocState({})

    self.M.propagate(S)

    assert_aequal(S.state, [
      [ 4.63617503e+00,  4.90314048e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0],
      [ 4.90314048e+00,  5.18979253e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00,  3.47549344e-01, -2.90072396e-02,  0.00000000e+00,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00, -2.90072396e-02,  3.47695722e-01,  0.00000000e+00,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  5.00000000e-01,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  6.00000000e-01, 0],
      [ 0,               0,               0,               0,               0,               0,              0]
    ], decimal=6)

  def test_solenoid(self):
    "Propagate a state matrix through a solenoid"

    T = self.expect = numpy.asfarray([
      [0.1, 0,   0,   0,   0,   0,   0],
      [0,   0.2, 0,   0,   0,   0,   0],
      [0,   0,   0.3, 0,   0,   0,   0],
      [0,   0,   0,   0.4, 0,   0,   0],
      [0,   0,   0,   0,   0.5, 0,   0],
      [0,   0,   0,   0,   0,   0.6, 0],
      [0,   0,   0,   0,   0,   0,   0]
    ])

    self.M = Machine({
      'sim_type':'MomentMatrix',
      'elements':[
        {'name':'elem0', 'type':'source', 'initial':T},
        {'name':'elem1', 'type':'solenoid', 'L':1.123, 'K':-1.0e3, 'B':0.0},
      ]
    })

    S = self.M.allocState({})

    self.M.propagate(S)

    assert_aequal(S.state, [
      [ 3.95745247e-01,  1.18242831e-02, -2.36485661e-02,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0],
      [ 1.18242831e-02,  2.98581749e-01, -1.73472348e-18, -2.36485661e-02,  0.00000000e+00,  0.00000000e+00, 0],
      [-2.36485661e-02,  0.00000000e+00,  2.01418251e-01,  1.18242831e-02,  0.00000000e+00,  0.00000000e+00, 0],
      [ 8.67361738e-19, -2.36485661e-02,  1.18242831e-02,  1.04254753e-01,  0.00000000e+00,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  5.00000000e-01,  0.00000000e+00, 0],
      [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  6.00000000e-01, 0],
      [ 0,               0,               0,               0,               0,               0,              0]
    ], decimal=6)

  def test_lat(self):
    # Propagate a state matrix through a lattice defined by a lattice file.
    P = GLPSParser()

    with open(os.path.join(datadir, 'moment_jb.lat'), 'rb') as inf:
        self.M = Machine(inf.read())

        S = self.M.allocState({})

        self.M.propagate(S)

        assert_aequal(S.state, [
          [ 3.15034165e+00,  9.27334719e-03,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0],
          [ 9.27334719e-03,  6.37581482e-03,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0],
          [ 0.00000000e+00,  0.00000000e+00,  1.59854625e+01,  4.96594365e+00,  0.00000000e+00,  0.00000000e+00, 0],
          [ 0.00000000e+00,  0.00000000e+00,  4.96594365e+00,  1.55019577e+00,  0.00000000e+00,  0.00000000e+00, 0],
          [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  5.00000000e-01,  0.00000000e+00, 0],
          [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  6.00000000e-01, 0],
          [ 0,               0,               0,               0,               0,               0,              0]
        ], decimal=6)

  def test_parse(self):
    "Test global scope when parsing"
    # Propagate a state matrix through a lattice defined by a lattice file.
    P = GLPSParser()

    with open(os.path.join(datadir, 'moment_jb_2.lat'), 'rb') as inf:
        self.M = Machine(inf.read())

        S = self.M.allocState({})

        self.M.propagate(S)

        assert_aequal(S.state, [
          [ 7.50527918e+00,  4.29398123e-03,  1.26662933e-02, -1.18523706e-06,  3.17367476e-04, -2.34554323e-05, 0],
          [ 4.29398123e-03,  3.84946607e-06, -2.41285106e-05, -1.85409878e-08,  1.06777952e-07,  5.28564016e-09, 0],
          [ 1.26662933e-02, -2.41285106e-05,  8.08978916e+00,  5.33808178e-03, -1.19544245e-03,  7.51043870e-05, 0],
          [-1.18523706e-06, -1.85409878e-08,  5.33808178e-03,  4.89711389e-06, -5.01614882e-07,  5.57484222e-08, 0],
          [ 3.17367476e-04,  1.06777952e-07, -1.19544245e-03, -5.01614882e-07,  6.71687185e-04, -1.23223342e-05, 0],
          [-2.34554323e-05,  5.28564016e-09,  7.51043870e-05,  5.57484222e-08, -1.23223342e-05,  1.99524669e-06, 0],
          [ 0,               0,               0,               0,               0,               0,              0]
        ], decimal=6)


  def test_LS1(self):
    "Propagate through LS1."
    PS_X = 0; PS_PX = 1; PS_Y = 2; PS_PY = 3; PS_S = 4; PS_PS = 5

    MeVtoeV = 1e6

    def sqr(a): return a*a;

    P = GLPSParser()

    file_name = 'latticeout_IMP_withPV_consolidate2.lat'

    with open(os.path.join(datadir, file_name), 'rb') as inf:
      M = Machine(inf.read())

      S = M.allocState({})
      M.propagate(S, 0, 1)
      S.moment0[:] = [-0.0007886,   1.08371e-05,  0.01337343,   6.678534e-06,  -0.0001847729, 0.000309995, 1.0];

      self.assertAlmostEqual(S.real_IonZ, 0.13865546218487396, 14)
      self.assertAlmostEqual(S.real_IonEs, 931494320.0, 14)
      self.assertAlmostEqual(S.real_IonEk, 500000.0, 14)
      self.assertAlmostEqual(S.real_IonW,  931994320.0, 14)

      self.assertAlmostEqual(S.ref_IonZ, 0.13865546218487396, 14)
      self.assertAlmostEqual(S.ref_IonEs, 931494320.0, 14)
      self.assertAlmostEqual(S.ref_IonEk, 500000.0, 14)
      self.assertAlmostEqual(S.ref_IonW,  931994320.0, 14)

      S.real_gamma     = S.real_IonW/S.real_IonEs;
      S.real_beta      = math.sqrt(1e0-1e0/sqr(S.real_gamma));
      S.real_bg        = S.real_beta*S.real_gamma;
      S.real_phis      = S.moment0[PS_S];
      S.real_Ekinetic += S.moment0[PS_PS]*MeVtoeV;

      def checkConsist(self, S, P='real', extra=False, skipbg=False):
          #self.assertEqual(getattr(S, P+'_IonW')    , getattr(S, P+'_IonEs')+getattr(S, P+'_IonEk'))
          self.assertEqual(getattr(S, P+'_gamma')   , getattr(S, P+'_IonW')/getattr(S, P+'_IonEs'))
          self.assertEqual(getattr(S, P+'_beta')    , math.sqrt(1e0-1e0/sqr(getattr(S, P+'_gamma'))))
          if not skipbg:
              self.assertEqual(getattr(S, P+'_bg')      , getattr(S, P+'_beta')*getattr(S, P+'_gamma'))
          if extra:
              self.assertEqual(getattr(S, P+'_phis')    , S.moment0[PS_S])
              self.assertEqual(getattr(S, P+'_Ekinetic'), getattr(S, P+'_IonEk') + S.moment0[PS_PS]*MeVtoeV)

      checkConsist(self, S, 'real', extra=True)
      checkConsist(self, S, 'ref')
      self.assertAlmostEqual(S.ref_phis,  0.0, 14)
      self.assertAlmostEqual(S.ref_Ekinetic,  S.ref_IonEk, 14)

      assert_aequal(S.moment0,
        [-7.88600000e-04, 1.08371000e-05, 1.33734300e-02, 6.67853400e-06, -1.84772900e-04, 3.09995000e-04, 1.00000000e+00],
      decimal=8)

      assert_aequal(S.state, [
        [ 2.76309450e+00, -4.28247337e-04,  1.58178569e-02,  2.15594191e-05,  1.86380506e-04, -2.99394487e-05,  0.00000000e+00],
        [-4.28247337e-04,  3.84946607e-06, -1.38385440e-06, -1.85409878e-08,  1.06777952e-07,  5.28564016e-09,  0.00000000e+00],
        [ 1.58178569e-02, -1.38385440e-06,  2.36251226e+00, -6.69320460e-04, -5.80099939e-04,  6.71651534e-06,  0.00000000e+00],
        [ 2.15594191e-05, -1.85409878e-08, -6.69320460e-04,  4.89711389e-06, -5.01614882e-07,  5.57484222e-08,  0.00000000e+00],
        [ 1.86380506e-04,  1.06777952e-07, -5.80099939e-04, -5.01614882e-07,  6.71687185e-04, -1.23223342e-05,  0.00000000e+00],
        [-2.99394487e-05,  5.28564016e-09,  6.71651534e-06,  5.57484222e-08, -1.23223342e-05,  1.99524669e-06,  0.00000000e+00],
        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00]
      ], decimal=8)

      M.propagate(S, 1, len(M))

      self.assertAlmostEqual(S.real_IonZ, 0.13865546218487396, 12)
      self.assertAlmostEqual(S.real_IonEs, 931494320.0, 12)
      self.assertAlmostEqual(S.real_IonEk, 500000.0, 12)
      self.assertAlmostEqual(S.real_IonW,  948584259.4594134, 12)

      self.assertAlmostEqual(S.ref_IonZ, 0.13865546218487396, 12)
      self.assertAlmostEqual(S.ref_IonEs, 931494320.0, 12)
      self.assertAlmostEqual(S.ref_IonEk, 500000.0, 12)
      self.assertAlmostEqual(S.ref_IonW,  948584732.218118, 12)

      checkConsist(self, S, 'real')
      self.assertAlmostEqual(S.real_phis,  1532.1994551432952, 14)
      self.assertAlmostEqual(S.real_Ekinetic,  17089939.45941341, 14)

      checkConsist(self, S, 'ref', skipbg=True)
      self.assertAlmostEqual(S.ref_bg,  0.03276937557631209, 14) # TODO: ref_bg isn't consistent w/ ref_gamma*ref_beta
      self.assertAlmostEqual(S.ref_phis,  1532.2018533339335, 14)
      self.assertAlmostEqual(S.ref_Ekinetic,  17090412.218117952, 14)

      assert_aequal(S.moment0,
        [-1.31487198e+00, -6.14116226e-04, -7.31682439e-01, -7.46618429e-04, -2.39819002e-03, -4.72758705e-04,  1.00000000e+00],
        decimal=8)

      assert_aequal(S.state, [
        [ 1.28985466e+00,  5.25768610e-04, -1.07818343e-01, -8.75275442e-05, -1.74466591e-04, -4.89638797e-05,  0.00000000e+00],
        [ 5.25768610e-04,  4.63230951e-07, -1.87620874e-04, -4.61354166e-08,  4.10553482e-08,  1.86305659e-08,  0.00000000e+00],
        [-1.07818343e-01, -1.87620874e-04,  2.54172968e+00,  4.50707865e-04,  2.29903897e-04,  1.14226041e-04,  0.00000000e+00],
        [-8.75275442e-05, -4.61354166e-08,  4.50707865e-04,  2.09807522e-07,  1.67123574e-07,  7.00281218e-08,  0.00000000e+00],
        [-1.74466591e-04,  4.10553482e-08,  2.29903897e-04,  1.67123574e-07,  3.45700733e-04,  1.29370100e-04,  0.00000000e+00],
        [-4.89638797e-05,  1.86305659e-08,  1.14226041e-04,  7.00281218e-08,  1.29370100e-04,  5.18511035e-05,  0.00000000e+00],
        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00]
      ], decimal=8)
