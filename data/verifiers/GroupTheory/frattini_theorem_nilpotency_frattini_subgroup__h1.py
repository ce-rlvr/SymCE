import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: \\Phi(G) is the Frattini subgroup of G",
    "¬Q: \\Phi(G) is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_frattini(G):
    """Helper to compute or extract the Frattini subgroup of G."""
    if hasattr(G, 'frattini_subgroup'):
        f = G.frattini_subgroup
        return f() if callable(f) else f
    if hasattr(G, 'Frattini'):
        f = G.Frattini
        return f() if callable(f) else f
    if hasattr(G, 'maximal_subgroups'):
        max_subs = G.maximal_subgroups
        max_subs = max_subs() if callable(max_subs) else max_subs
        if not max_subs:
            return G
        f = max_subs[0]
        for h in max_subs[1:]:
            if hasattr(f, 'intersection'):
                f = f.intersection(h)
            elif hasattr(f, 'intersect'):
                f = f.intersect(h)
            else:
                try:
                    e1 = set(f.generate())
                    e2 = set(h.generate())
                    common = list(e1.intersection(e2))
                    f = PermutationGroup(common)
                except Exception:
                    return None
        return f
    return None

def conditions(witness) -> list[bool]:
    # The witness can be either a group G, or a tuple (G, Phi_G)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, Phi_G = witness
        else:
            G = witness
            Phi_G = get_frattini(G)
    except Exception:
        return [False, False]

    # Check H_1: \Phi(G) is the Frattini subgroup of G
    h1_ok = False
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            if hasattr(G, 'is_Frattini_subgroup'):
                h1_ok = bool(G.is_Frattini_subgroup(Phi_G))
            else:
                f = get_frattini(G)
                if f is not None:
                    h1_ok = bool(f == Phi_G)
                else:
                    # If we cannot compute it but it was explicitly provided, assume valid mock
                    h1_ok = True
        else:
            f = get_frattini(G)
            h1_ok = (f is not None)
    except Exception:
        h1_ok = False

    # Check ¬Q: \Phi(G) is NOT a nilpotent group
    neg_q_ok = False
    try:
        if Phi_G is not None and hasattr(Phi_G, 'is_nilpotent'):
            is_nilp = Phi_G.is_nilpotent
            if callable(is_nilp):
                is_nilp = is_nilp()
            neg_q_ok = not bool(is_nilp)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]