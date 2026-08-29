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

def check_prop(witness, *names, default=False):
    if isinstance(witness, dict):
        for name in names:
            if name in witness:
                return bool(witness[name])
    else:
        for name in names:
            if hasattr(witness, name):
                return bool(getattr(witness, name))
    return default

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) >= 3 and all(isinstance(x, bool) for x in witness[:3]):
        try:
            h1 = bool(witness[0])
            h2 = bool(witness[1])
            neg_q = not bool(witness[2])
            return [h1, h2, neg_q]
        except Exception:
            pass

    try:
        h1 = check_prop(witness, 'R_integrally_closed', 'is_integrally_closed', 'integrally_closed', default=False)
    except Exception:
        h1 = False

    try:
        h2 = check_prop(witness, 'L_finite_separable', 'is_finite_separable', 'finite_separable', 'finite_separable_extension', default=False)
    except Exception:
        h2 = False

    try:
        q_not_fin_gen = check_prop(witness, 'integral_closure_not_finitely_generated', 'not_finitely_generated', default=False)
        q_not_noeth = check_prop(witness, 'integral_closure_not_Noetherian', 'not_Noetherian', default=False)
        
        if q_not_fin_gen or q_not_noeth:
            neg_q = True
        else:
            q_fin_gen = check_prop(witness, 'integral_closure_finitely_generated', 'is_finitely_generated', 'finitely_generated', default=True)
            q_noeth = check_prop(witness, 'integral_closure_Noetherian', 'is_Noetherian', 'Noetherian', default=True)
            neg_q = not (q_fin_gen and q_noeth)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is integrally closed in its field of fractions K",
    "H_2: L is a finite separable field extension of K",
    "¬Q: The integral closure of R in L is not a finitely generated R-module, or is not Noetherian"
]

N_HYP = 2
NEG_Q_INDEX = 2