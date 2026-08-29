import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import Matrix
import itertools
import math
import functools

# Top-level setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: u is an element of R",
    "¬Q: u is a unit in R but not in R^op, or vice versa"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (R, u) where R is a ring and u is an element.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        R, u = witness
    except Exception:
        return [False, False, False]

    def check_h1():
        if getattr(R, 'is_Ring', False) or getattr(R, 'is_ring', False):
            return True
        try:
            elements = []
            for i, x in enumerate(R):
                if i > 1000:  # Prevent infinite loops for infinite iterables
                    return False
                elements.append(x)
            if not elements:
                return False
            
            # Check for multiplicative identity
            has_id = False
            for e in elements:
                if all(e * x == x and x * e == x for x in elements):
                    has_id = True
                    break
            if not has_id:
                return False
                
            # Check closure under ring operations
            for a in elements:
                for b in elements:
                    if (a + b) not in elements: return False
                    if (a * b) not in elements: return False
                    if (a - b) not in elements: return False
            return True
        except Exception:
            pass
        return False

    def check_h2():
        try:
            if hasattr(R, '__contains__'):
                if u in R:
                    return True
        except Exception:
            pass
        try:
            return u in list(R)
        except Exception:
            pass
        return False

    def check_neg_q():
        def is_unit_R(u, R):
            if hasattr(R, 'is_unit'):
                return bool(R.is_unit(u))
            try:
                elements = list(R)
                id_R = None
                for e in elements:
                    if all(e * x == x and x * e == x for x in elements):
                        id_R = e
                        break
                if id_R is None:
                    return False
                for v in elements:
                    if u * v == id_R and v * u == id_R:
                        return True
                return False
            except Exception:
                return False

        def is_unit_R_op(u, R):
            if hasattr(R, 'is_unit'):
                return bool(R.is_unit(u))
            try:
                elements = list(R)
                id_R = None
                for e in elements:
                    if all(e * x == x and x * e == x for x in elements):
                        id_R = e
                        break
                if id_R is None:
                    return False
                for v in elements:
                    # In R^op, the product u *_{op} v is defined as v * u in R.
                    # Thus, u is a unit in R^op iff there exists v such that
                    # v * u == id_R and u * v == id_R.
                    if v * u == id_R and u * v == id_R:
                        return True
                return False
            except Exception:
                return False

        unit_R = is_unit_R(u, R)
        unit_R_op = is_unit_R_op(u, R)
        
        # The conclusion is: u is a unit in R iff u is a unit in R^op.
        # We return True if the conclusion FAILS.
        return unit_R != unit_R_op

    try:
        h1 = check_h1()
    except Exception:
        h1 = False

    try:
        h2 = check_h2()
    except Exception:
        h2 = False

    try:
        neg_q = check_neg_q()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]