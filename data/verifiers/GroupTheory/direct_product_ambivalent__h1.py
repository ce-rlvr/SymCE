import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def is_ambivalent(G):
    """
    Checks if a group G is ambivalent.
    A group is ambivalent if every element is conjugate to its inverse.
    """
    try:
        elements = list(G.generate())
        for g in elements:
            g_inv = g**-1
            # Check if there exists x in G such that x * g * x^-1 == g^-1
            if not any(x * g * x**-1 == g_inv for x in elements):
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Given a witness (G, H), checks the hypotheses and the negated conclusion.
    Order of return: [H_1, H_2, neg_Q]
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is an ambivalent group
    h1 = is_ambivalent(G)
    
    # H_2: H is an ambivalent group
    h2 = is_ambivalent(H)
    
    # Q: The direct product G x H is an ambivalent group
    # We check if every element (g, h) in G x H is conjugate to its inverse (g^-1, h^-1).
    # This is equivalent to checking if g is conjugate to g^-1 in G, and h is conjugate to h^-1 in H.
    try:
        elems_G = list(G.generate())
        elems_H = list(H.generate())
        q = True
        for g in elems_G:
            for h in elems_H:
                g_inv = g**-1
                h_inv = h**-1
                
                found_x = any(x * g * x**-1 == g_inv for x in elems_G)
                found_y = any(y * h * y**-1 == h_inv for y in elems_H)
                
                if not (found_x and found_y):
                    q = False
                    break
            if not q:
                break
    except Exception:
        # If we cannot evaluate Q, we return False for neg_Q
        q = True
        
    return [h1, h2, not q]

CONDITION_LABELS = [
    "H_1: G is an ambivalent group",
    "H_2: H is an ambivalent group",
    "¬Q: The direct product G x H is not an ambivalent group"
]

N_HYP = 2
NEG_Q_INDEX = 2