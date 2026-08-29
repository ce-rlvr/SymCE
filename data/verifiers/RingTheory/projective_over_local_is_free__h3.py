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

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def check_prop(obj, prop_names, default=False):
    if isinstance(obj, dict):
        for p in prop_names:
            if p in obj:
                return bool(obj[p])
    for p in prop_names:
        try:
            if hasattr(obj, p):
                val = getattr(obj, p)
                if callable(val):
                    return bool(val())
                else:
                    return bool(val)
        except Exception:
            continue
    return default

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
            h1 = check_prop(R, ['is_commutative_ring', 'is_commutative'])
            h2 = check_prop(R, ['is_local_ring', 'is_local'])
            h3 = check_prop(M, ['is_projective_module', 'is_projective'])
            is_free = check_prop(M, ['is_free_module', 'is_free'], default=True)
            neg_q = not is_free
        else:
            h1 = check_prop(witness, ['is_commutative_ring', 'is_commutative', 'R_is_commutative'])
            h2 = check_prop(witness, ['is_local_ring', 'is_local', 'R_is_local'])
            h3 = check_prop(witness, ['is_projective_module', 'is_projective', 'M_is_projective'])
            is_free = check_prop(witness, ['is_free_module', 'is_free', 'M_is_free'], default=True)
            neg_q = not is_free
            
        if isinstance(witness, str):
            s = witness.lower()
            h1 = h1 or ('commutative' in s)
            h2 = h2 or ('local' in s)
            h3 = h3 or ('projective' in s)
            if not neg_q:
                neg_q = ('not free' in s or 'non-free' in s or "isn't free" in s)
                
    except Exception:
        pass
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring",
    "H_3: M is a projective R-module",
    "¬Q: M is not a free R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3