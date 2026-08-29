import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H1: H is a subgroup of G
    try:
        h1 = bool(H.is_subgroup(G))
    except Exception:
        h1 = False
        
    # H2: The normalizer N_G(H) has finite index in G
    try:
        if not h1:
            h2 = False
        else:
            if hasattr(G, 'order') and G.order() != sympy.oo:
                h2 = True
            else:
                h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The number of distinct conjugate subgroups of H in G is NOT exactly the index of N_G(H) in G.
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            h_elements = list(H.generate())
            h_elements_set = set(h_elements)
            conjugates = set()
            n_g_h_size = 0
            
            for g in G.generate():
                try:
                    conj = frozenset(tuple((g * h * g**-1).array_form) for h in h_elements)
                except AttributeError:
                    conj = frozenset(g * h * g**-1 for h in h_elements)
                conjugates.add(conj)
                
                is_in_normalizer = True
                for h in H.generators:
                    if (g * h * g**-1) not in h_elements_set:
                        is_in_normalizer = False
                        break
                if is_in_normalizer:
                    n_g_h_size += 1
                    
            num_conjugates = len(conjugates)
            index = G.order() // n_g_h_size
            
            neg_q = bool(num_conjugates != index)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The normalizer N_G(H) has finite index in G",
    "¬Q: The number of distinct conjugate subgroups of H in G is NOT exactly the index of N_G(H) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2