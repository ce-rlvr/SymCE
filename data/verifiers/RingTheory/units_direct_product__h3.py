import math
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: R1 is a ring with multiplicative identity",
    "H_2: R2 is a ring with multiplicative identity",
    "¬Q: U(R1 x R2) is not isomorphic to U(R1) x U(R2)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        
        R1, R2 = witness
        
        h1 = False
        h2 = False
        
        domain_rings = [ZZ, QQ, RR, CC]
        
        # Check if R1 is a ring with identity (integers n >= 0 represent Z/nZ)
        if isinstance(R1, int) and R1 >= 0:
            h1 = True
        elif R1 in domain_rings:
            h1 = True
            
        # Check if R2 is a ring with identity
        if isinstance(R2, int) and R2 >= 0:
            h2 = True
        elif R2 in domain_rings:
            h2 = True
            
        # Evaluate the conclusion
        if h1 and h2 and isinstance(R1, int) and isinstance(R2, int):
            def get_U_orders(n):
                if n == 0:
                    return [1, 2] # U(Z) = {1, -1}
                if n == 1:
                    return [1]    # U(Z/1Z) = {0}
                units = [i for i in range(1, n) if math.gcd(i, n) == 1]
                orders = []
                for u in units:
                    order = 1
                    curr = u % n
                    while curr != 1:
                        curr = (curr * u) % n
                        order += 1
                    orders.append(order)
                return sorted(orders)
                
            orders1 = get_U_orders(R1)
            orders2 = get_U_orders(R2)
            
            # Orders of elements in the direct product of groups U(R1) x U(R2)
            prod_orders = []
            for o1 in orders1:
                for o2 in orders2:
                    prod_orders.append(lcm(o1, o2))
            prod_orders.sort()
            
            # The units of R1 x R2 are pairs (u1, u2) where u1 in U(R1) and u2 in U(R2).
            # The order of (u1, u2) is lcm(order(u1), order(u2)).
            # Thus, the multiset of orders of U(R1 x R2) is exactly prod_orders.
            U_R1xR2_orders = prod_orders.copy()
            
            isomorphic = (prod_orders == U_R1xR2_orders)
            neg_q = not isomorphic
        else:
            # For other valid rings, U(R1 x R2) is categorically isomorphic to U(R1) x U(R2)
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]