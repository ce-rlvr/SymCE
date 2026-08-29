import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
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

def get_bool(witness, names, default=False):
    if isinstance(witness, dict):
        for name in names:
            if name in witness:
                val = witness[name]
                return bool(val()) if callable(val) else bool(val)
    else:
        for name in names:
            if hasattr(witness, name):
                val = getattr(witness, name)
                return bool(val()) if callable(val) else bool(val)
    return default

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False

    # Try to unpack as (R, Q, P)
    R, Q, P = None, None, None
    if isinstance(witness, tuple) and len(witness) == 3:
        R, Q, P = witness
    elif isinstance(witness, dict) and 'R' in witness and 'Q' in witness and 'P' in witness:
        R, Q, P = witness['R'], witness['Q'], witness['P']
    elif hasattr(witness, 'R') and hasattr(witness, 'Q') and hasattr(witness, 'P'):
        R, Q, P = witness.R, witness.Q, witness.P

    if R is not None and Q is not None and P is not None:
        try:
            h1_val = getattr(R, 'is_commutative', False) or getattr(R, 'is_commutative_ring', False)
            h1 = bool(h1_val() if callable(h1_val) else h1_val)
        except Exception:
            h1 = False

        try:
            is_prim = getattr(Q, 'is_primary', False)
            if callable(is_prim): is_prim = is_prim()
            rad = getattr(Q, 'radical', None)
            if callable(rad): rad = rad()
            h2 = bool(is_prim and rad == P)
        except Exception:
            h2 = False

        try:
            h3 = bool(Q != P)
        except Exception:
            h3 = False

        try:
            quot = getattr(Q, 'ideal_quotient', None)
            if quot is not None:
                q_p = quot(P)
                q_holds = bool(q_p != Q)
                neg_q = not q_holds
            else:
                q_holds = get_bool(witness, ['quotient_strictly_contains', 'quotient_strictly_contains_Q'], default=True)
                neg_q = not q_holds
        except Exception:
            neg_q = False

        if h1 or h2 or h3 or neg_q:
            return [h1, h2, h3, neg_q]

    # Fallback to dictionary/object properties
    try:
        h1 = get_bool(witness, ['is_commutative_ring', 'is_commutative'])
    except Exception:
        h1 = False

    try:
        h2 = get_bool(witness, ['is_P_primary', 'is_primary', 'Q_is_P_primary'])
    except Exception:
        h2 = False

    try:
        h3 = get_bool(witness, ['Q_neq_P', 'Q_not_equal_P'])
    except Exception:
        h3 = False

    try:
        q_holds = get_bool(witness, ['quotient_strictly_contains', 'quotient_strictly_contains_Q', 'ideal_quotient_strictly_contains'], default=True)
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Q is a P-primary ideal in R",
    "H_3: Q != P",
    "¬Q: The ideal quotient (Q:P) does not strictly contain Q"
]

N_HYP = 3
NEG_Q_INDEX = 3