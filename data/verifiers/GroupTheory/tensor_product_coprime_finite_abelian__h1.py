import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS: list[str] = [
    "H_1: B is a finite abelian group of order n",
    "H_2: m and n are coprime integers",
    "¬Q: The tensor product A \\otimes_\\mathbb{Z} B is not the trivial group"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2

def conditions(witness) -> list[bool]:
    try:
        A, B, m, n = witness
    except Exception:
        return [False, False, False]
        
    def get_inv(G):
        if hasattr(G, 'abelian_invariants'):
            invs = G.abelian_invariants
            if callable(invs):
                invs = invs()
            return [int(x) for x in invs]
        elif isinstance(G, (list, tuple)):
            return [int(x) for x in G]
        elif isinstance(G, int) or (hasattr(G, 'is_Integer') and G.is_Integer):
            return [int(G)]
        return None

    # H1: B is a finite abelian group of order n
    try:
        n_val = int(n)
        if hasattr(B, 'is_abelian') and hasattr(B, 'order'):
            is_ab = B.is_abelian
            if callable(is_ab):
                is_ab = is_ab()
            order_val = B.order
            if callable(order_val):
                order_val = order_val()
            h1 = bool(is_ab and order_val == n_val)
        else:
            inv_B = get_inv(B)
            if inv_B is not None:
                if inv_B == []:
                    h1 = (n_val == 1)
                else:
                    h1 = True
                    prod = 1
                    for x in inv_B:
                        if x < 1:
                            h1 = False
                        prod *= x
                    if h1:
                        h1 = (prod == n_val)
            else:
                h1 = False
    except Exception:
        h1 = False
        
    # H2: m and n are coprime integers
    try:
        m_val = int(m)
        n_val = int(n)
        h2 = (math.gcd(m_val, n_val) == 1)
    except Exception:
        h2 = False
        
    # neg_Q: A \otimes B is NOT the trivial group
    try:
        inv_A = get_inv(A)
        inv_B = get_inv(B)
            
        if inv_A is not None and inv_B is not None:
            is_trivial = True
            for a in inv_A:
                for b in inv_B:
                    if math.gcd(a, b) != 1:
                        is_trivial = False
                        break
                if not is_trivial:
                    break
            neg_q = not is_trivial
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]