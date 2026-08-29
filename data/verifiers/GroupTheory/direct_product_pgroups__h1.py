import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
        p, G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: p is a prime number
    try:
        h1 = sympy.ntheory.isprime(p)
    except Exception:
        h1 = False
        
    # neg_Q: The direct product G x H is a p-group if and only if both G and H are p-groups.
    # Note: A standard trap in this theorem is the trivial group. If a p-group is defined 
    # as having order p^k for k >= 1 (excluding the trivial group), then G x {e} is a p-group 
    # but {e} is not, breaking the "only if" direction.
    try:
        def is_p_group(order, p):
            try:
                order = int(order)
                p = int(p)
            except Exception:
                return False
            # Exclude the trivial group (order 1) from being a p-group
            if order < p:
                return False
            while order % p == 0:
                order //= p
            return order == 1
            
        order_G = G.order()
        order_H = H.order()
        order_GH = order_G * order_H
        
        gh_is_p = is_p_group(order_GH, p)
        g_is_p = is_p_group(order_G, p)
        h_is_p = is_p_group(order_H, p)
        
        # The conclusion is the equivalence: gh_is_p == (g_is_p and h_is_p)
        # We want the negated conclusion (i.e., the equivalence fails)
        neg_q = not (gh_is_p == (g_is_p and h_is_p))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The equivalence (G x H is a p-group iff both G and H are p-groups) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1
