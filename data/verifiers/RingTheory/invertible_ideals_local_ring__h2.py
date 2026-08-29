import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
class FiniteRing:
    """
    A helper class to represent finite rings and check their properties.
    """
    def __init__(self, elements, add_func, mul_func, zero, one):
        self.elements = elements
        self.add_func = add_func
        self.mul_func = mul_func
        self.zero = zero
        self.one = one

    def is_commutative(self):
        for a in self.elements:
            for b in self.elements:
                if self.mul_func(a, b) != self.mul_func(b, a):
                    return False
        return True

    def is_local(self):
        units = set()
        for a in self.elements:
            for b in self.elements:
                if self.mul_func(a, b) == self.one:
                    units.add(a)
                    break
        
        non_units = [x for x in self.elements if x not in units]
        
        # In a commutative ring, the non-units form an ideal iff they are closed under addition.
        for a in non_units:
            for b in non_units:
                if self.add_func(a, b) not in non_units:
                    return False
        return True

    def ideal_generated_by(self, gens):
        if not isinstance(gens, (list, tuple, set)):
            gens = [gens]
        elif len(gens) > 0 and isinstance(gens[0], int):
            gens = [gens]
            
        ideal = {self.zero}
        for g in gens:
            new_ideal = set(ideal)
            for r in self.elements:
                prod = self.mul_func(r, g)
                for elem in ideal:
                    new_ideal.add(self.add_func(elem, prod))
            ideal = new_ideal
        return ideal

    def is_principal(self, gens):
        I = self.ideal_generated_by(gens)
        for r in self.elements:
            if self.ideal_generated_by([r]) == I:
                return True
        return False

# Define the local ring F_2[x,y]/(x^2, xy, y^2)
# Elements are represented as tuples (a, b, c) corresponding to a + bx + cy
_elements = [(a,b,c) for a in (0,1) for b in (0,1) for c in (0,1)]
def _add(e1, e2): return ((e1[0]+e2[0])%2, (e1[1]+e2[1])%2, (e1[2]+e2[2])%2)
def _mul(e1, e2): return ((e1[0]*e2[0])%2, (e1[0]*e2[1] + e1[1]*e2[0])%2, (e1[0]*e2[2] + e1[2]*e2[0])%2)

LocalRing_F2_xy_mod_m2 = FiniteRing(_elements, _add, _mul, (0,0,0), (1,0,0))
LocalRing_F2_xy_mod_m2.x = (0,1,0)
LocalRing_F2_xy_mod_m2.y = (0,0,1)

# Standard bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Expected witness format: a tuple (R, I_gens) where R is a ring and I_gens is a list of generators.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get("ring", witness.get("R"))
            I_gens = witness.get("ideal", witness.get("I", witness.get("I_gens")))
        else:
            R, I_gens = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(R.is_commutative() and R.is_local())
    except Exception:
        h1 = False
        
    try:
        # The conclusion is that I is a principal fractional ideal.
        # We want the negation: I is NOT a principal fractional ideal.
        neg_q = not bool(R.is_principal(I_gens))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative local ring",
    "¬Q: I is not a principal fractional ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1