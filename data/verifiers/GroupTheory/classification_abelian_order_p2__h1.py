import math
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    # H_1: G is an abelian group
    try:
        h1 = bool(witness.is_abelian)
    except Exception:
        h1 = False

    # H_2: The order of G is p^2
    try:
        order = int(witness.order())
        p = math.isqrt(order)
        h2 = (p * p == order) and (order > 0)
    except Exception:
        h2 = False

    # ¬Q: G is NOT isomorphic to either Z/p^2Z or (Z/pZ) x (Z/pZ)
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            order = int(witness.order())
            p = math.isqrt(order)
            
            # Get elements of the witness group
            try:
                elements = list(witness.elements)
            except Exception:
                elements = list(witness.generate())
                
            # Element orders of the witness group
            g_orders = sorted([int(g.order()) for g in elements])
            
            # Element orders of Z/p^2Z
            z_p2_orders = sorted([order // math.gcd(k, order) for k in range(order)])
            
            # Element orders of (Z/pZ) x (Z/pZ)
            def lcm(a, b):
                return (a * b) // math.gcd(a, b)
                
            orders_p = [p // math.gcd(k, p) for k in range(p)]
            z_p_x_z_p_orders = sorted([lcm(oa, ob) for oa in orders_p for ob in orders_p])
            
            # Check for isomorphism by comparing the multiset of element orders
            is_z_p2 = (g_orders == z_p2_orders)
            is_z_p_x_z_p = (g_orders == z_p_x_z_p_orders)
            
            neg_q = not (is_z_p2 or is_z_p_x_z_p)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: The order of G is p^2",
    "¬Q: G is not isomorphic to either Z/p^2Z or (Z/pZ) x (Z/pZ)"
]

N_HYP = 2
NEG_Q_INDEX = 2