import sympy
from sympy.abc import x, y, z, t, u, v, w
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def conditions(witness) -> list[bool]:
    try:
        gens = None
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[1], (list, tuple)):
            gens = witness[1]
        elif hasattr(witness, 'gens'):
            gens = witness.gens
        elif isinstance(witness, (list, tuple)):
            gens = witness
        
        if gens is not None:
            h1 = True
            for w_elem in gens:
                if not (hasattr(w_elem, 'free_symbols') or hasattr(w_elem, 'parent') or isinstance(w_elem, (int, float, sympy.Expr))):
                    h1 = False
                    break
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if not h1 or gens is None:
            neg_q = False
        elif len(gens) <= 1:
            neg_q = False
        else:
            if hasattr(gens[0], 'ring'):
                ring = gens[0].ring
                ideal = ring.ideal(*gens)
                gb = ideal.groebner()
                neg_q = len(gb) > 1
            else:
                from sympy import groebner
                has_symbols = any(hasattr(g, 'free_symbols') and g.free_symbols for g in gens)
                if not has_symbols:
                    neg_q = False
                else:
                    gb = groebner(gens)
                    neg_q = len(gb) > 1
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is a finitely generated ideal of R",
    "¬Q: I is not a principal ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1