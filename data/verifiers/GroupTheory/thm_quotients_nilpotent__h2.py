import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_subgroup(group, sub):
    try:
        if hasattr(sub, 'is_subgroup'):
            res = sub.is_subgroup(group)
            if callable(res):
                res = res()
            return bool(res)
    except Exception:
        pass
    
    if not hasattr(sub, 'generators'):
        return False
    
    try:
        for gen in sub.generators:
            if gen not in group:
                return False
        return True
    except Exception:
        return False

def is_normal_subgroup(group, sub):
    if not is_subgroup(group, sub):
        return False
    
    try:
        if hasattr(sub, 'is_normal'):
            res = sub.is_normal(group)
            if callable(res):
                res = res()
            return bool(res)
    except Exception:
        pass
    
    try:
        for g in group.generators:
            g_inv = ~g
            for n in sub.generators:
                if (g * n * g_inv) not in sub:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, N = witness
    except Exception:
        return [False, False]

    # H_1: G is a nilpotent group
    try:
        h1_val = G.is_nilpotent
        if callable(h1_val):
            h1_val = h1_val()
        h1_ok = bool(h1_val)
    except Exception:
        h1_ok = False

    # ¬Q: The quotient group G/N is not nilpotent
    try:
        # If N is not a normal subgroup, G/N is not a valid group, hence not a nilpotent group.
        if not is_subgroup(G, N):
            q = False
        elif not is_normal_subgroup(G, N):
            q = False
        else:
            # For a normal subgroup N, G/N is nilpotent iff the lower central series of G 
            # eventually falls into N.
            lcs = G.lower_central_series
            if callable(lcs):
                lcs = lcs()
            last_lcs = lcs[-1]
            q = is_subgroup(N, last_lcs)
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: The quotient group G/N is not nilpotent"
]

N_HYP = 1
NEG_Q_INDEX = 1