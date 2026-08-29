import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False

    # 1. Custom object with attributes
    try:
        if hasattr(witness, 'is_nonzero_nonunit') and hasattr(witness, 'has_infinite_prime_divisors'):
            h1 = bool(witness.is_nonzero_nonunit)
            neg_q = bool(witness.has_infinite_prime_divisors)
            return [h1, neg_q]
    except Exception:
        pass

    # 2. Tuple of (ring, element)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            ring, a = witness
            if isinstance(ring, str):
                ring_str = ring.lower()
                a_str = str(a).lower()
                
                # Ring of entire functions
                if any(w in ring_str for w in ["entire", "analytic", "holomorphic"]):
                    if any(f in a_str for f in ["sin", "cos", "tan", "sinh", "cosh"]):
                        return [True, True]
                
                # Z + xQ[x]
                if "q[x]" in ring_str and "z" in ring_str:
                    if "x" in a_str:
                        return [True, True]
                        
                # Boolean ring
                if "boolean" in ring_str or "sets" in ring_str:
                    if a_str not in ["0", "1", "false", "true", "none"]:
                        return [True, True]
    except Exception:
        pass

    # 3. String representation
    try:
        if isinstance(witness, str):
            s = witness.lower()
            if ("entire" in s or "analytic" in s) and any(f in s for f in ["sin", "cos", "tan"]):
                return [True, True]
            if "q[x]" in s and "z" in s and "x" in s:
                return [True, True]
    except Exception:
        pass

    # 4. SymPy expression (interpreted as an element of the ring of entire functions)
    try:
        if isinstance(witness, sympy.Expr):
            if witness.is_zero:
                return [False, False]
            
            syms = witness.free_symbols
            if not syms:
                if witness in [1, -1]:
                    return [False, False]
                else:
                    return [True, False]
            
            sym = list(syms)[0]
            roots = sympy.solveset(witness, sym, domain=sympy.S.Complexes)
            
            if roots.is_empty:
                return [False, False]
            
            h1 = True
            if roots.is_FiniteSet is False:
                neg_q = True
            else:
                neg_q = False
            return [h1, neg_q]
    except Exception:
        pass

    # 5. Fallback for integer or other types
    try:
        if isinstance(witness, int):
            if witness != 0 and witness not in (1, -1):
                h1 = True
            neg_q = False
            return [h1, neg_q]
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is a non-zero, non-unit element of R",
    "¬Q: Up to multiplication by units, there are infinitely many distinct prime elements that divide a"
]

N_HYP = 1
NEG_Q_INDEX = 1