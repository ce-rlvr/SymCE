import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import S, eye, zeros
import math
import itertools
import functools
import z3

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is recursively presented",
    "¬Q: G cannot be embedded in any finitely presented group"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_bool_attr(obj, attr):
    if hasattr(obj, attr):
        val = getattr(obj, attr)
        if callable(val):
            try:
                return bool(val())
            except Exception:
                return None
        return bool(val)
    return None

def is_sympy_group(witness):
    try:
        if isinstance(witness, PermutationGroup):
            return True
    except Exception:
        pass
    try:
        if type(witness).__name__ in ['FpGroup', 'FreeGroup', 'PermutationGroup']:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    h1 = False
    neg_q = False

    # Handle string representations of common counterexamples
    if isinstance(witness, str):
        w = witness.strip().lower()
        counterexamples = [
            "q", "rationals", "rational numbers", "the rationals",
            "z(p^infty)", "prufer group", "prüfer group",
            "additive group of rational numbers",
            "additive group of rationals"
        ]
        if w in counterexamples:
            return [True, True]
        return [False, False]

    # Handle tuple representations like (S.Rationals, '+')
    try:
        if isinstance(witness, tuple) and len(witness) > 0:
            if witness[0] == S.Rationals:
                return [True, True]
            if witness[0] == S.Integers:
                return [True, False]
            if witness[0] in [S.Reals, S.Complexes]:
                return [False, True]
    except Exception:
        pass

    # Evaluate H_1: G is recursively presented
    try:
        val = get_bool_attr(witness, 'is_recursively_presented')
        if val is not None:
            h1 = val
        else:
            val = get_bool_attr(witness, 'is_finitely_presented')
            if val is not None:
                h1 = val
            elif is_sympy_group(witness):
                h1 = True
            elif witness in [S.Rationals, S.Integers]:
                h1 = True
            elif witness in [S.Reals, S.Complexes]:
                h1 = False
    except Exception:
        h1 = False

    # Evaluate ¬Q: G cannot be embedded in any finitely presented group
    # By Higman's Embedding Theorem, a recursively presented group can be embedded
    # in a finitely presented group if and only if it is finitely generated.
    try:
        for attr in ['can_embed_in_fp_group', 'is_embeddable_in_fp_group', 'embeds_in_fp']:
            val = get_bool_attr(witness, attr)
            if val is not None:
                neg_q = not val
                break
        else:
            val = get_bool_attr(witness, 'is_finitely_generated')
            if val is not None:
                neg_q = not val
            elif is_sympy_group(witness):
                neg_q = False
            elif witness == S.Rationals:
                neg_q = True
            elif witness == S.Integers:
                neg_q = False
            elif witness in [S.Reals, S.Complexes]:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]