import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: c(X) denotes the number of conjugacy classes of a group X
    # We interpret this as the witness being a valid PermutationGroup.
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    # neg_Q: The number of conjugacy classes of G is NOT the product of the 
    # number of conjugacy classes of its simple factors.
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            cc_attr = witness.conjugacy_classes
            if callable(cc_attr):
                cc = cc_attr()
            else:
                cc = cc_attr
            c_G = len(cc)
            
            is_solv_attr = witness.is_solvable
            if callable(is_solv_attr):
                is_solv = is_solv_attr()
            else:
                is_solv = is_solv_attr
                
            order_attr = witness.order
            if callable(order_attr):
                order = order_attr()
            else:
                order = order_attr
                
            # For solvable groups, the composition factors are cyclic groups of prime order.
            # The number of conjugacy classes of Z_p is p.
            # Thus, the product of c(S_i) for all composition factors is exactly the product 
            # of the primes, which equals the order of the group.
            if is_solv:
                prod_c_Si = order
            else:
                # Fallback for some known non-solvable groups
                if order == 60: # A5
                    prod_c_Si = 5
                elif order == 120: # S5
                    prod_c_Si = 10
                elif order == 360: # A6
                    prod_c_Si = 7
                elif order == 720: # S6
                    prod_c_Si = 14
                else:
                    raise NotImplementedError("prod_c_Si not implemented for this non-solvable group")
            
            neg_q_ok = bool(c_G != prod_c_Si)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: c(X) denotes the number of conjugacy classes of a group X",
    "¬Q: c(G) is not the product of the number of conjugacy classes of its simple factors"
]

N_HYP = 1
NEG_Q_INDEX = 1