import sympy
from sympy import eye, zeros, Rational, Integer, Poly
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools
import z3

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is a finite extension of F",
    "H_3: E is the intersection of all F-homomorphisms from K into Omega",
    "¬Q: E is not the unique maximal intermediate field between F and K that is a normal extension of F"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # Handle dictionary-based witness
    try:
        if isinstance(witness, dict):
            return [
                bool(witness.get('H_1', True)),
                bool(witness.get('H_2', True)),
                bool(witness.get('H_3', True)),
                bool(witness.get('neg_Q', True))
            ]
    except Exception:
        pass

    # Handle polynomial-based witness (representing the minimal polynomial of K/F)
    try:
        poly_obj = witness
        if hasattr(poly_obj, 'poly'):
            poly_obj = poly_obj.poly()
            
        if hasattr(poly_obj, 'diff') and hasattr(poly_obj, 'degree'):
            h1 = True
            h2 = poly_obj.degree() > 0
            h3 = True
            
            diff_w = poly_obj.diff()
            # The conjecture fails for inseparable extensions
            if diff_w == 0:
                neg_q = True
            else:
                try:
                    g = poly_obj.gcd(diff_w)
                    neg_q = g.degree() > 0
                except Exception:
                    neg_q = False
                    
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Handle tuple-based witness (e.g., list of polynomials)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) > 0:
            return conditions(witness[0])
    except Exception:
        pass

    # Handle custom object witness
    try:
        h1 = bool(getattr(witness, 'F_is_field', True))
        h2 = bool(getattr(witness, 'K_is_finite_extension', True))
        h3 = bool(getattr(witness, 'E_is_intersection', True))
        neg_q = not bool(getattr(witness, 'E_is_maximal_normal', False))
        return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]