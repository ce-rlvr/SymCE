import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, k), checks if it is a valid counterexample to the conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, k = witness
    except Exception:
        return [False, False]
        
    # H_1: Let k >= 1 be an integer
    try:
        h1_ok = type(k) is int and k >= 1
    except Exception:
        h1_ok = False
        
    # neg_Q: The k-th derived subgroup G^(k) is NOT a subgroup of the 2^k-th lower central subgroup \gamma_{2^k}(G)
    try:
        ds = G.derived_series()
        lcs = G.lower_central_series()
        
        # G^(k) is the k-th term in the derived series (0-indexed: G^(0) = G)
        if k < len(ds):
            G_k = ds[k]
        else:
            G_k = ds[-1]
            
        # \gamma_{2^k}(G) is the (2^k - 1)-th term in the lower central series (0-indexed: \gamma_1(G) = G)
        idx = 2**k - 1
        if idx < len(lcs):
            gamma = lcs[idx]
        else:
            gamma = lcs[-1]
            
        # Check if G_k is a subgroup of gamma
        if hasattr(G_k, 'is_subgroup'):
            is_subgroup = G_k.is_subgroup(gamma)
        else:
            is_subgroup = all(g in gamma for g in G_k.generators)
            
        neg_q_ok = not is_subgroup
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: k >= 1 is an integer",
    "¬Q: G^(k) is not a subgroup of gamma_{2^k}(G)"
]

N_HYP = 1
NEG_Q_INDEX = 1