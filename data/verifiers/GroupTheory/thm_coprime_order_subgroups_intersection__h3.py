import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        if hasattr(K, 'elements'):
            k_elements = set(K.elements)
            k_order = K.order()
        else:
            k_elements = set(K)
            k_order = len(k_elements)
    except Exception:
        k_elements = set()
        k_order = 0

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: H is a finite subgroup of G
    try:
        if isinstance(H, PermutationGroup):
            try:
                h2 = H.is_subgroup(G)
            except AttributeError:
                h2 = all(G.contains(g) for g in H.generators)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: The greatest common divisor of |H| and |K| is 1
    try:
        h_order = H.order()
        h3 = math.gcd(h_order, k_order) == 1
    except Exception:
        h3 = False
        
    # ¬Q: The intersection H \cap K is not the trivial subgroup {e}
    try:
        h_elements = set(H.elements)
        intersection = h_elements.intersection(k_elements)
        
        identity = None
        for p in h_elements:
            if p.is_Identity:
                identity = p
                break
                
        neg_q = (intersection != {identity})
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a finite subgroup of G",
    "H_3: The greatest common divisor of |H| and |K| is 1",
    "¬Q: The intersection H \\cap K is not the trivial subgroup {e}"
]

N_HYP = 3
NEG_Q_INDEX = 3