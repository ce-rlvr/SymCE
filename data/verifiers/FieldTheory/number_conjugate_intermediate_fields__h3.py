import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Witness is expected to be a tuple (G, H, S) where:
      - G is the Galois group (PermutationGroup)
      - H is the pointwise stabilizer of E
      - S is the setwise stabilizer of E
    Alternatively, (G, H) where H is the setwise stabilizer (S=H).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, H, S = witness
            elif len(witness) == 2:
                G, H = witness
                S = H
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    def is_subgroup(sub, sup):
        try:
            return all(g in sup for g in sub.generators)
        except Exception:
            return False

    # H_1: L/K is a finite Galois extension
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False
        
    # H_2: G is the Galois group of L/K
    try:
        h2 = h1
    except Exception:
        h2 = False
        
    # H_3: H is the subgroup of G fixing E
    try:
        h3 = False
        if isinstance(H, PermutationGroup) and isinstance(S, PermutationGroup):
            if is_subgroup(H, G) and is_subgroup(S, G) and is_subgroup(H, S):
                is_normal = True
                for s in S.generators:
                    for h in H.generators:
                        if (s * h * ~s) not in H:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h3 = is_normal
    except Exception:
        h3 = False
        
    # neg_Q: The number of distinct intermediate fields conjugate to E over K is not equal to the index of N_G(H) in G
    try:
        # The actual number of conjugates of E is the index of S in G
        num_conjugates = G.order() // S.order()
        
        # Compute the normalizer of H in G, N_G(H)
        elements = list(G.generate())
        normalizer_size = 0
        for g in elements:
            if all((g * h * ~g) in H for h in H.generators):
                normalizer_size += 1
                
        index_normalizer = G.order() // normalizer_size
        
        # The conclusion fails if the actual number of conjugates is not equal to the index of N_G(H) in G
        neg_q = (num_conjugates != index_normalizer)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: G is the Galois group of L/K",
    "H_3: H is the subgroup of G fixing E",
    "neg_Q: The number of distinct intermediate fields conjugate to E over K is not equal to the index of N_G(H) in G"
]

N_HYP = 3
NEG_Q_INDEX = 3