import math
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            m = witness.get('m')
            G = witness.get('G')
            H = witness.get('H')
        else:
            n, m, G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: n and m are positive integers
    try:
        h1 = type(n) is int and type(m) is int and n > 0 and m > 0
    except Exception:
        h1 = False

    # H_2: G is the cyclic group Z/nZ
    try:
        h2 = False
        if hasattr(G, 'order') and hasattr(G, 'elements'):
            g_order = G.order() if callable(G.order) else G.order
            if g_order == n:
                for g in G.elements:
                    elem_order = g.order() if callable(g.order) else g.order
                    if elem_order == n:
                        h2 = True
                        break
    except Exception:
        h2 = False

    # neg_Q: The abelian group of homomorphisms Hom(G, H) is NOT isomorphic to Z/gcd(n,m)Z
    try:
        if not hasattr(H, 'elements') or not hasattr(H, 'identity'):
            neg_q = False
        else:
            h_id = H.identity() if callable(H.identity) else H.identity
            S = [h for h in H.elements if h**n == h_id]
            
            is_abelian_group = True
            for h1_elem in S:
                for h2_elem in S:
                    if h1_elem * h2_elem != h2_elem * h1_elem:
                        is_abelian_group = False
                        break
                if not is_abelian_group:
                    break
                    
            if not is_abelian_group:
                q = False
            else:
                target_order = math.gcd(n, m)
                if len(S) != target_order:
                    q = False
                else:
                    q = False
                    for h in S:
                        elem_order = h.order() if callable(h.order) else h.order
                        if elem_order == target_order:
                            q = True
                            break
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n and m are positive integers",
    "H_2: G is the cyclic group Z/nZ",
    "¬Q: The abelian group of homomorphisms Hom(G, H) is not isomorphic to Z/gcd(n,m)Z"
]

N_HYP = 2
NEG_Q_INDEX = 2