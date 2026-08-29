import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False]
        
    # H_1: H is a subgroup of G
    try:
        h1 = H.is_subgroup(G)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = N.is_normal(G)
    except Exception:
        h2 = False
        
    # Conclusion: HN is a subgroup of G, H \cap N is a normal subgroup of H, and HN/N \cong H/(H \cap N)
    try:
        # Compute HN elements
        HN_elements = set()
        for h in H.generate():
            for n in N.generate():
                HN_elements.add(h * n)
                
        G_elements = set(G.generate())
        if not HN_elements.issubset(G_elements):
            HN_is_subgroup = False
        else:
            HN_list = list(HN_elements)
            HN_gen = PermutationGroup(HN_list)
            if HN_gen.order() != len(HN_elements):
                HN_is_subgroup = False
            else:
                HN_is_subgroup = True
                
        # Compute H \cap N
        H_elements = set(H.generate())
        N_elements = set(N.generate())
        H_int_N_elements = H_elements.intersection(N_elements)
        H_int_N = PermutationGroup(list(H_int_N_elements))
        
        is_H_int_N_normal = H_int_N.is_normal(H)
        
        # For HN/N to be a valid quotient group, N must be normal in HN
        if HN_is_subgroup:
            is_N_normal_in_HN = N.is_normal(HN_gen)
        else:
            is_N_normal_in_HN = False
            
        # If HN is a subgroup, H \cap N is normal in H, and N is normal in HN,
        # the natural map is an isomorphism, so HN/N \cong H/(H \cap N) holds.
        conclusion = HN_is_subgroup and is_H_int_N_normal and is_N_normal_in_HN
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: N is a normal subgroup of G",
    "¬Q: HN is not a subgroup of G, or H \\cap N is not normal in H, or HN/N is not isomorphic to H/(H \\cap N)"
]

N_HYP = 2
NEG_Q_INDEX = 2