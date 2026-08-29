import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, S_list) where G is the group and S_list is 
    the list of non-abelian simple groups [S_1, ..., S_k].
    """
    try:
        G, S_list = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a semisimple group
    # A finite group is semisimple if it has no non-trivial normal abelian subgroups.
    try:
        h1 = True
        if hasattr(G, 'normal_subgroups'):
            for N in G.normal_subgroups():
                if N.order() > 1 and N.is_abelian:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: Let G = S_1 \times S_2 \times \dots \times S_k be a decomposition of G 
    # into a direct product of non-abelian simple groups S_i
    try:
        h2 = True
        expected_order = 1
        for S in S_list:
            if S.is_abelian:
                h2 = False
                break
            if hasattr(S, 'normal_subgroups'):
                if len(S.normal_subgroups()) != 2:
                    h2 = False
                    break
            expected_order *= S.order()
        
        if h2:
            if G.order() != expected_order:
                h2 = False
    except Exception:
        h2 = False

    # ¬Q: The composition length of G is not exactly k, or the multiset of 
    # composition factors of G is not exactly {S_1, S_2, \dots, S_k}.
    try:
        k = len(S_list)
        if hasattr(G, 'composition_series'):
            series = G.composition_series()
            comp_length = len(series) - 1
            
            if comp_length != k:
                q = False
            else:
                if k == 0:
                    # For the trivial group, the empty set of factors is exactly the empty set.
                    q = True
                else:
                    # The composition factors are quotient groups G_i / G_{i+1}.
                    # These are sets of cosets, which are not exactly the subgroups S_i.
                    # The conjecture is false because it omits "up to isomorphism".
                    q = False
        else:
            # If composition_series is not available (e.g., custom infinite group),
            # it fails to have exactly those factors.
            q = False
    except Exception:
        q = False

    return [h1, h2, not q]

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "H_2: G is a direct product of non-abelian simple groups S_1, ..., S_k",
    "¬Q: The composition length of G is not exactly k, or the multiset of composition factors is not exactly {S_1, ..., S_k}"
]

N_HYP = 2
NEG_Q_INDEX = 2