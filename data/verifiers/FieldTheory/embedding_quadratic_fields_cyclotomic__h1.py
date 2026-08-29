import sympy
from sympy import Poly
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
import sympy.ntheory
import z3
import math
import itertools
import functools

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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, sympy.Expr) and x not in witness.free_symbols:
            try:
                p = sympy.minpoly(witness, x, polys=True)
                if p.degree() == 2:
                    h1 = True
                    neg_q = False
                    return [h1, neg_q]
            except Exception:
                pass
                
        p = Poly(witness, x, domain='QQ')
        if p.degree() == 2:
            h1 = True
            if not p.is_irreducible:
                neg_q = True
            else:
                neg_q = False
                
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The degree of K over Q is exactly 2",
    "¬Q: K is not contained in a cyclotomic field"
]

N_HYP = 1
NEG_Q_INDEX = 1