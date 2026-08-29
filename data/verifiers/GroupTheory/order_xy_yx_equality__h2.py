import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros, Matrix

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

def conditions(witness) -> list[bool]:
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False, False]
        
    h1, h2, h3, neg_q = False, False, False, False

    # Try PermutationGroup first
    try:
        if hasattr(G, 'is_group') and G.is_group:
            h1 = True
            h2 = y in G
            xy = x * y
            n = xy.order()
            h3 = True
            yx = y * x
            neg_q = (yx.order() != n)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Fallback to list/tuple of elements (e.g., matrices)
    try:
        if isinstance(G, (list, tuple)) and len(G) > 0:
            e_G = None
            # Find identity
            for e in G:
                if all(e * a == a and a * e == a for a in G):
                    e_G = e
                    break
            
            if e_G is not None:
                closed = True
                inverses = True
                for a in G:
                    has_inv = False
                    for b in G:
                        prod = a * b
                        if not any(prod == g for g in G):
                            closed = False
                        if prod == e_G and b * a == e_G:
                            has_inv = True
                    if not has_inv:
                        inverses = False
                h1 = closed and inverses
                
                h2 = any(y == g for g in G)
                
                xy = x * y
                curr = xy
                n = None
                for i in range(1, 100):
                    if curr == e_G:
                        n = i
                        break
                    curr = curr * xy
                h3 = (n is not None)
                
                if h3:
                    yx = y * x
                    curr = yx
                    yx_order = None
                    for i in range(1, 100):
                        if curr == e_G:
                            yx_order = i
                            break
                        curr = curr * yx
                    neg_q = (yx_order != n)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: y is an element of G",
    "H_3: the product xy has a finite order n",
    "¬Q: the product yx does not have finite order n"
]

N_HYP = 3
NEG_Q_INDEX = 3