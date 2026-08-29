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

def extract_bool(witness, names, default=None):
    if isinstance(witness, dict):
        for name in names:
            if name in witness:
                v = witness[name]
                return bool(v() if callable(v) else v)
    for name in names:
        if hasattr(witness, name):
            try:
                v = getattr(witness, name)
                return bool(v() if callable(v) else v)
            except Exception:
                pass
    if hasattr(witness, '__getitem__'):
        for name in names:
            try:
                v = witness[name]
                return bool(v() if callable(v) else v)
            except Exception:
                pass
    return default

def conditions(witness) -> list[bool]:
    if callable(witness):
        try:
            witness = witness()
        except Exception:
            pass

    h1 = extract_bool(witness, [
        'is_continuous_bilinear', 'continuous_bilinear', 'is_bilinear_and_continuous',
        'B_is_continuous_bilinear'
    ], None)
    
    h2 = extract_bool(witness, [
        'U_is_bounded', 'is_U_bounded', 'U_bounded'
    ], None)
    
    h3 = extract_bool(witness, [
        'V_is_bounded', 'is_V_bounded', 'V_bounded'
    ], None)
    
    is_lip = extract_bool(witness, [
        'is_Lipschitz', 'Lipschitz_continuous', 'is_Lipschitz_on_UxV', 'is_lipschitz'
    ], None)

    if isinstance(witness, tuple) and len(witness) >= 3:
        B, U, V = witness[:3]
        if h1 is None:
            h1 = extract_bool(B, ['is_continuous_bilinear', 'is_continuous', 'is_bilinear'], False)
        if h2 is None:
            h2 = extract_bool(U, ['is_bounded', 'bounded'], False)
        if h3 is None:
            h3 = extract_bool(V, ['is_bounded', 'bounded'], False)
        if is_lip is None:
            is_lip = extract_bool(B, ['is_Lipschitz_on_UxV', 'is_Lipschitz', 'is_lipschitz'], True)

    if h1 is None: h1 = False
    if h2 is None: h2 = False
    if h3 is None: h3 = False
    if is_lip is None: is_lip = True

    neg_q = not is_lip

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: B is a continuous bilinear map",
    "H_2: U is a bounded subset",
    "H_3: V is a bounded subset",
    "¬Q: The restriction of B to U x V is not Lipschitz continuous"
]

N_HYP = 3
NEG_Q_INDEX = 3