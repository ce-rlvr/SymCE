import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H, a, b = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a group
    try:
        if hasattr(G, 'elements'):
            G_elements = set(G.elements)
            h1 = True
        elif isinstance(G, (set, frozenset, list, tuple)):
            G_elements = set(G)
            h1 = len(G_elements) > 0
            is_closed = True
            for g1 in G_elements:
                for g2 in G_elements:
                    if g1 * g2 not in G_elements:
                        is_closed = False
                        break
                if not is_closed:
                    break
            h1 = h1 and is_closed
        else:
            h1 = False
            G_elements = set()
    except Exception:
        h1 = False
        G_elements = set()

    # H_2: H is a subgroup of G
    try:
        if hasattr(H, 'elements'):
            H_elements = set(H.elements)
        elif isinstance(H, (set, frozenset, list, tuple)):
            H_elements = set(H)
        else:
            H_elements = set()
            
        h2 = len(H_elements) > 0 and H_elements.issubset(G_elements)
        is_closed = True
        for h_1 in H_elements:
            for h_2 in H_elements:
                if h_1 * h_2 not in H_elements:
                    is_closed = False
                    break
            if not is_closed:
                break
        h2 = h2 and is_closed
    except Exception:
        h2 = False
        H_elements = set()

    # H_3: a is an element of G
    try:
        h3 = a in G_elements
    except Exception:
        h3 = False

    # neg_Q: The left coset aH is equal to the left coset bH if and only if a^{-1}b is an element of H
    try:
        # Compute aH
        if isinstance(a, (set, frozenset, list, tuple)):
            aH = set(x * h for x in a for h in H_elements)
        else:
            aH = set(a * h for h in H_elements)
            
        # Compute bH
        if isinstance(b, (set, frozenset, list, tuple)):
            bH = set(x * h for x in b for h in H_elements)
        else:
            bH = set(b * h for h in H_elements)
            
        left_eq = (aH == bH)
        
        # Compute a^{-1}b
        try:
            a_inv = ~a
        except Exception:
            a_inv = a**(-1)
            
        if isinstance(b, (set, frozenset, list, tuple)):
            a_inv_b = frozenset(a_inv * x for x in b)
        else:
            a_inv_b = a_inv * b
            
        # Check if a^{-1}b is in H
        try:
            right_in = (a_inv_b in H_elements)
        except TypeError:
            right_in = False
            
        neg_q = (left_eq != right_in)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: a is an element of G",
    "¬Q: (aH == bH) is not equivalent to (a^{-1}b in H)"
]

N_HYP = 3
NEG_Q_INDEX = 3