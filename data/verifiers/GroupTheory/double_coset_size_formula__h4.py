import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4) # V4 is often represented as a subgroup of A4, but we provide A4 as a base
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: K is a subgroup of G",
    "¬Q: The cardinality of the double coset H x K is NOT equal to |H||K| / |H \\cap x K x^{-1}|"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        G, H, K, x = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() < float('inf')
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H_3: K is a subgroup of G
    try:
        h3 = isinstance(K, PermutationGroup) and K.is_subgroup(G)
    except Exception:
        h3 = False

    # ¬Q: The cardinality of the double coset H x K is NOT equal to |H||K| / |H \cap x K x^{-1}|
    try:
        # Generate elements of H and K
        H_elems = list(H.generate_dimino())
        K_elems = list(K.generate_dimino())
        
        # Compute the double coset H x K
        HxK = set()
        for h in H_elems:
            for k in K_elems:
                HxK.add(h * x * k)
                
        # Compute x K x^{-1}
        xKx_inv = set()
        x_inv = ~x
        for k in K_elems:
            xKx_inv.add(x * k * x_inv)
            
        # Compute the intersection H \cap x K x^{-1}
        H_set = set(H_elems)
        intersection = H_set.intersection(xKx_inv)
        
        # Check if the formula holds
        expected_size = (len(H_elems) * len(K_elems)) / len(intersection)
        neg_q = len(HxK) != expected_size
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]