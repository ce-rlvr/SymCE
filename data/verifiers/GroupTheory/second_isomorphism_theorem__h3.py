import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, H, N).
    """
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: H is a subgroup of G
    try:
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            h2 = all(g in G for g in H.generators)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: HN is not a subgroup of G, or H \cap N is not normal in H, or HN/N is not isomorphic to H/(H \cap N)
    try:
        Q = True
        if not (isinstance(H, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup)):
            Q = False
        else:
            H_els = list(H.generate())
            N_els = list(N.generate())
            
            HN_set = set(h * n for h in H_els for n in N_els)
            
            # 1. HN is a subgroup of G
            if G.identity not in HN_set:
                Q = False
            else:
                subset = True
                for a in HN_set:
                    if a not in G:
                        subset = False
                        break
                if not subset:
                    Q = False
                else:
                    closed = True
                    for a in HN_set:
                        for b in HN_set:
                            if a * b not in HN_set:
                                closed = False
                                break
                        if not closed:
                            break
                    if not closed:
                        Q = False
                    else:
                        HN = PermutationGroup(list(HN_set))
                        
                        # 2. H \cap N is a normal subgroup of H
                        H_cap_N_set = set(H_els).intersection(set(N_els))
                        H_cap_N = PermutationGroup(list(H_cap_N_set))
                        if not H_cap_N.is_normal(H):
                            Q = False
                        else:
                            # 3. HN/N \cong H/(H \cap N)
                            # For the quotient group HN/N to be well-defined and the isomorphism to hold,
                            # N must be a normal subgroup of HN.
                            if not N.is_normal(HN):
                                Q = False
                            else:
                                Q = True
        neg_q = not Q
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: HN is not a subgroup of G, or H \\cap N is not normal in H, or HN/N is not isomorphic to H/(H \\cap N)"
]

N_HYP = 2
NEG_Q_INDEX = 2