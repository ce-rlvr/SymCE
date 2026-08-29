import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            if hasattr(H, 'is_subgroup') and H.is_subgroup(G):
                h2 = True
            else:
                H_elems = list(H.generate_dimino()) if hasattr(H, 'generate_dimino') else list(H.elements)
                G_elems = list(G.generate_dimino()) if hasattr(G, 'generate_dimino') else list(G.elements)
                
                max_deg = max(G.degree, H.degree)
                def pad(p):
                    arr = p.array_form
                    return tuple(arr) + tuple(range(len(arr), max_deg))
                
                G_set = set(pad(g) for g in G_elems)
                H_set = set(pad(h) for h in H_elems)
                h2 = H_set.issubset(G_set)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The set product HN is not a subgroup of G
    try:
        H_elems = list(H.generate_dimino()) if hasattr(H, 'generate_dimino') else list(H)
        N_elems = list(N.generate_dimino()) if hasattr(N, 'generate_dimino') else list(N)
        
        HN = set()
        for h in H_elems:
            for n in N_elems:
                HN.add(h * n)
        
        if not HN:
            is_subgroup = False
        else:
            is_subgroup = True
            for x in HN:
                if ~x not in HN:
                    is_subgroup = False
                    break
                for y in HN:
                    if x * y not in HN:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
        neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: The set product HN is not a subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2