import sympy
from sympy import Poly, discriminant
from sympy.abc import x
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
import math

# Top-level setup for potential witness expressions
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
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    # H_1: K is the splitting field of f(x) over Q
    # We verify that the witness is a valid polynomial over the Rationals.
    try:
        if not isinstance(witness, (sympy.Expr, sympy.Poly)):
            h1 = False
        else:
            syms = witness.free_symbols
            if len(syms) != 1:
                h1 = False
            else:
                sym = list(syms)[0]
                f = Poly(witness, sym)
                h1 = all(c.is_Rational for c in f.coeffs()) and f.degree() >= 1
    except Exception:
        h1 = False

    # neg_Q: The Galois group Gal(K/Q) is NOT isomorphic to the alternating group A_5
    try:
        if not h1:
            neg_q = False
        else:
            sym = list(witness.free_symbols)[0]
            f = Poly(witness, sym)
            deg = f.degree()
            
            if deg < 5:
                is_A5 = False
            elif deg == 5:
                if not f.is_irreducible:
                    is_A5 = False
                else:
                    disc = sympy.Rational(discriminant(f, sym))
                    if disc <= 0:
                        is_A5 = False
                    else:
                        num = disc.p
                        den = disc.q
                        if math.isqrt(num)**2 != num or math.isqrt(den)**2 != den:
                            is_A5 = False
                        else:
                            is_A5 = True
            else:
                is_A5 = False
            
            neg_q = not is_A5
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over the Rationals",
    "¬Q: The Galois group Gal(K/Q) is not isomorphic to the alternating group A_5"
]

N_HYP = 1
NEG_Q_INDEX = 1