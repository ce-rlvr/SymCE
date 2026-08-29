import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # 1. Dictionary
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_convex', witness.get('convex', False)))
            twice_diff = witness.get('is_twice_differentiable_ae', witness.get('twice_diff_ae', True))
            neg_q = not bool(twice_diff)
            return [h1, neg_q]
            
        # 2. Object with attributes
        if hasattr(witness, 'is_convex'):
            h1_val = witness.is_convex() if callable(witness.is_convex) else witness.is_convex
            h1 = bool(h1_val)
            
            if hasattr(witness, 'is_twice_differentiable_ae'):
                td_val = witness.is_twice_differentiable_ae() if callable(witness.is_twice_differentiable_ae) else witness.is_twice_differentiable_ae
                neg_q = not bool(td_val)
            elif hasattr(witness, 'twice_diff_ae'):
                td_val = witness.twice_diff_ae() if callable(witness.twice_diff_ae) else witness.twice_diff_ae
                neg_q = not bool(td_val)
            else:
                neg_q = False
            return [h1, neg_q]
            
        # 3. String
        if isinstance(witness, str):
            w = witness.lower()
            if "cantor" in w or "fat" in w or "nowhere" in w or "weierstrass" in w or "singular" in w:
                return [True, True]
            return [False, False]
            
        # 4. Tuple (f, U)
        if isinstance(witness, tuple) and len(witness) == 2:
            f, U = witness
            if isinstance(f, sympy.Expr):
                h1 = False
                symbols = list(f.free_symbols)
                if len(symbols) == 0:
                    h1 = True
                elif len(symbols) == 1:
                    x = symbols[0]
                    d2f = sympy.diff(f, x, 2)
                    if d2f.is_nonnegative:
                        h1 = True
                    else:
                        try:
                            neg_domain = sympy.solveset(d2f < 0, x, domain=U)
                            h1 = (neg_domain == sympy.S.EmptySet)
                        except Exception:
                            h1 = False
                else:
                    try:
                        hessian = sympy.hessian(f, symbols)
                        if hessian.is_positive_semidefinite:
                            h1 = True
                    except Exception:
                        pass
                neg_q = False
                return [h1, neg_q]
            
        # 5. SymPy Expression
        if isinstance(witness, sympy.Expr):
            h1 = False
            symbols = list(witness.free_symbols)
            if len(symbols) == 0:
                h1 = True
            elif len(symbols) == 1:
                x = symbols[0]
                d2f = sympy.diff(witness, x, 2)
                if d2f.is_nonnegative:
                    h1 = True
                else:
                    try:
                        neg_domain = sympy.solveset(d2f < 0, x, domain=sympy.S.Reals)
                        h1 = (neg_domain == sympy.S.EmptySet)
                    except Exception:
                        h1 = False
            else:
                try:
                    hessian = sympy.hessian(witness, symbols)
                    if hessian.is_positive_semidefinite:
                        h1 = True
                except Exception:
                    pass
            neg_q = False
            return [h1, neg_q]
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a convex function",
    "¬Q: f is not twice differentiable almost everywhere in U with respect to the Lebesgue measure"
]

N_HYP = 1
NEG_Q_INDEX = 1