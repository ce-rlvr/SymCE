import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: G is isomorphic to a direct product of non-abelian simple groups
    try:
        if isinstance(G, PermutationGroup) and G.order() > 1:
            series = G.composition_series()
            factors_count = len(series) - 1
            # For groups with <= 5 composition factors, having only non-abelian simple 
            # composition factors is strictly equivalent to being a direct product of them.
            if factors_count <= 5:
                h2 = True
                for i in range(factors_count):
                    q_order = series[i].order() // series[i+1].order()
                    # A composition factor is non-abelian simple iff its order is not prime
                    if isprime(q_order):
                        h2 = False
                        break
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: H is not a normal subgroup of G
    try:
        is_sub = H.is_subgroup(G)
        if is_sub:
            is_norm = H.is_normal(G)
        else:
            is_norm = False
        # The conclusion fails if H is a valid subgroup but NOT normal in G
        neg_q = is_sub and not is_norm
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is isomorphic to a direct product of non-abelian simple groups",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2