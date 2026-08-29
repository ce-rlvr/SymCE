import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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
    Checks if the witness is a counterexample to the conjecture.
    The witness can be a group G, or a tuple (G, k).
    """
    if isinstance(witness, tuple):
        if len(witness) == 2:
            G, k_val = witness
            k_list = [k_val]
        else:
            return [False, False]
    else:
        G = witness
        # If no specific k is provided, we check a reasonable range of k
        k_list = range(1, 10)
        
    # H_1: Let G be a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # neg_Q: The k-th derived subgroup G^(k) is NOT a subgroup of the 2^k-th lower central subgroup gamma_{2^k}(G)
    neg_q = False
    if h1:
        try:
            lcs = G.lower_central_series()
            ds = G.derived_series()
            
            for k in k_list:
                if not isinstance(k, (int, sympy.Integer)) or k < 0:
                    continue
                k = int(k)
                
                # Get G^(k)
                if k < len(ds):
                    G_k = ds[k]
                else:
                    G_k = ds[-1]
                    
                # Get gamma_{2^k}(G)
                # Note: lcs[0] is gamma_1, lcs[1] is gamma_2, ..., lcs[n-1] is gamma_n
                idx = 2**k - 1
                if idx < len(lcs):
                    gamma_2k = lcs[idx]
                else:
                    gamma_2k = lcs[-1]
                    
                # Check if G_k is a subgroup of gamma_2k
                # A group is a subgroup if all its generators are in the parent group
                is_sub = all(g in gamma_2k for g in G_k.generators)
                
                if not is_sub:
                    neg_q = True
                    break
        except Exception:
            neg_q = False
            
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The k-th derived subgroup G^(k) is not a subgroup of the 2^k-th lower central subgroup gamma_{2^k}(G)"
]

N_HYP = 1
NEG_Q_INDEX = 1