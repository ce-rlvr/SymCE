import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
try:
    from sympy.combinatorics import DirectProduct
except ImportError:
    from sympy.combinatorics.group_constructs import DirectProduct
from sympy.matrices import eye, zeros
from itertools import permutations

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

def conditions(witness):
    """
    witness should be a tuple: (G, S_list, T_list)
    where G is a PermutationGroup, and S_list, T_list are lists of PermutationGroups.
    Alternatively, it can be (S_list, T_list), in which case G is taken to be the direct product of S_list.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, S_list, T_list = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            S_list, T_list = witness
            if not S_list:
                G = trivial
            elif len(S_list) == 1:
                G = S_list[0]
            else:
                G = DirectProduct(*S_list)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def get_dp(g_list):
        if not g_list:
            return trivial
        if len(g_list) == 1:
            return g_list[0]
        return DirectProduct(*g_list)

    # H_1: G is isomorphic to the direct product of S_1, ..., S_k, which are non-abelian simple groups
    h1_ok = False
    try:
        DP_S = get_dp(S_list)
        if G.is_isomorphic(DP_S):
            h1_ok = True
            for S in S_list:
                if S.is_abelian or len(S.normal_subgroups()) != 2:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # H_2: G is isomorphic to the direct product of T_1, ..., T_m, which are non-abelian simple groups
    h2_ok = False
    try:
        DP_T = get_dp(T_list)
        if G.is_isomorphic(DP_T):
            h2_ok = True
            for T in T_list:
                if T.is_abelian or len(T.normal_subgroups()) != 2:
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False

    # ¬Q: The factorizations are not equivalent (either k != m or factors are not isomorphic up to permutation)
    neg_q = False
    try:
        if len(S_list) != len(T_list):
            neg_q = True
        else:
            match_found = False
            for p in permutations(T_list):
                match = True
                for s, t in zip(S_list, p):
                    if not s.is_isomorphic(t):
                        match = False
                        break
                if match:
                    match_found = True
                    break
            neg_q = not match_found
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is isomorphic to the direct product of S_1, ..., S_k, which are non-abelian simple groups",
    "H_2: G is isomorphic to the direct product of T_1, ..., T_m, which are non-abelian simple groups",
    "¬Q: The factorizations are not equivalent (either k != m or factors are not isomorphic up to permutation)"
]

N_HYP = 2
NEG_Q_INDEX = 2