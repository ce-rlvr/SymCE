import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_nilpotent(g):
    if hasattr(g, 'is_nilpotent'):
        val = g.is_nilpotent
        res = val() if callable(val) else val
        if res is None:
            raise ValueError("is_nilpotent is None")
        return bool(res)
    raise AttributeError("is_nilpotent not found")

def is_solvable(g):
    if hasattr(g, 'is_solvable'):
        val = g.is_solvable
        res = val() if callable(val) else val
        if res is None:
            raise ValueError("is_solvable is None")
        return bool(res)
    raise AttributeError("is_solvable not found")

def get_proper_subgroups(g):
    if hasattr(g, 'proper_subgroups'):
        val = g.proper_subgroups
        return val() if callable(val) else val
    if hasattr(g, 'subgroups'):
        val = g.subgroups
        subs = val() if callable(val) else val
        proper = []
        for h in subs:
            if hasattr(h, 'order') and hasattr(g, 'order'):
                h_ord = h.order() if callable(h.order) else h.order
                g_ord = g.order() if callable(g.order) else g.order
                if h_ord < g_ord:
                    proper.append(h)
            elif h != g:
                proper.append(h)
        return proper
    raise AttributeError("subgroups not found")

def check_every_proper_subgroup_nilpotent(g):
    if hasattr(g, 'every_proper_subgroup_is_nilpotent'):
        val = g.every_proper_subgroup_is_nilpotent
        res = val() if callable(val) else val
        if res is not None:
            return bool(res)
    if hasattr(g, 'proper_subgroups_are_nilpotent'):
        val = g.proper_subgroups_are_nilpotent
        res = val() if callable(val) else val
        if res is not None:
            return bool(res)
    
    proper_subs = get_proper_subgroups(g)
    for h in proper_subs:
        if not is_nilpotent(h):
            return False
    return True

def conditions(witness) -> list[bool]:
    # H_1: Assume that G is not a nilpotent group.
    try:
        h1_ok = not is_nilpotent(witness)
    except Exception:
        h1_ok = False

    # H_2: Assume that every proper subgroup of G is a nilpotent group.
    try:
        h2_ok = check_every_proper_subgroup_nilpotent(witness)
    except Exception:
        h2_ok = False

    # ¬Q: G is not a solvable group.
    try:
        neg_q_ok = not is_solvable(witness)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is not a nilpotent group",
    "H_2: Every proper subgroup of G is a nilpotent group",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2