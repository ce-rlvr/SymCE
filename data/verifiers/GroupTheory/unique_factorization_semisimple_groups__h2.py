import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, DirectProduct, PermutationGroup
)
from sympy.matrices import eye, zeros

# Standard group bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard matrix bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is isomorphic to T_1 x ... x T_m, where each T_j is a non-abelian simple group",
    "¬Q: It is not the case that k = m and S_i is isomorphic to T_sigma(i) for some permutation sigma"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            S_list = witness.get('S', witness.get('S_list'))
            T_list = witness.get('T', witness.get('T_list'))
        else:
            G, S_list, T_list = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = (getattr(G, 'is_group', False) or isinstance(G, PermutationGroup)) and G.order() < float('inf')
    except Exception:
        h1 = False

    # H_2: G \cong T_1 \times \dots \times T_m, where each T_j is a non-abelian simple group
    try:
        h2 = True
        for T in T_list:
            if getattr(T, 'is_abelian', True):
                h2 = False
                break
            # A group is simple iff it has exactly 2 normal subgroups (itself and the trivial group)
            ns = T.normal_subgroups()
            if len(ns) != 2:
                h2 = False
                break
        
        if h2:
            if len(T_list) == 0:
                h2 = (G.order() == 1)
            elif len(T_list) == 1:
                h2 = G.is_isomorphic(T_list[0])
            else:
                DP = DirectProduct(*T_list)
                h2 = G.is_isomorphic(DP)
    except Exception:
        h2 = False

    # ¬Q: It is not the case that k = m and S_i is isomorphic to T_sigma(i) for some permutation sigma
    try:
        k = len(S_list)
        m = len(T_list)
        if k != m:
            q = False
        else:
            unmatched_T = list(T_list)
            q = True
            for S in S_list:
                match_found = False
                for i, T in enumerate(unmatched_T):
                    if S.is_isomorphic(T):
                        unmatched_T.pop(i)
                        match_found = True
                        break
                if not match_found:
                    q = False
                    break
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]