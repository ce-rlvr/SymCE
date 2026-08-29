import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: Let H be a subgroup of G.
    try:
        if not hasattr(H, 'is_subgroup'):
            h1 = False
        else:
            h1 = bool(H.is_subgroup(G))
    except Exception:
        h1 = False
        
    # neg_Q: The number of distinct subgroups of G that are conjugate to H is NOT equal to the index of N_G(H) in G.
    try:
        H_elements = frozenset(H.elements)
        conjugates = set()
        normalizer_elements = []
        
        for g in G.elements:
            # Compute the conjugate subgroup g * H * g^-1
            conj_elements = frozenset([g * h * ~g for h in H.elements])
            conjugates.add(conj_elements)
            
            # Check if g is in the normalizer N_G(H)
            if conj_elements == H_elements:
                normalizer_elements.append(g)
                
        num_conjugates = len(conjugates)
        normalizer_order = len(normalizer_elements)
        
        # Calculate the index of N_G(H) in G
        index = int(G.order()) // normalizer_order
        
        neg_q = bool(num_conjugates != index)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = ["H_1: H is a subgroup of G", "¬Q: The number of distinct subgroups of G conjugate to H is not equal to the index of N_G(H) in G"]
N_HYP = 1
NEG_Q_INDEX = 1