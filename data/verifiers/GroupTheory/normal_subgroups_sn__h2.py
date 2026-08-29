import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, PermutationGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: n is an integer with n >= 5
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, N = witness
        else:
            N = witness
            n = N.degree
        
        h1_ok = isinstance(n, int) and n >= 5
    except Exception:
        h1_ok = False

    # H_2: N is a normal subgroup of S_n
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, N = witness
        else:
            N = witness
            n = N.degree
            
        if not isinstance(N, PermutationGroup):
            h2_ok = False
        else:
            Sn = SymmetricGroup(n)
            
            # Check if N is a subgroup of Sn
            is_subgroup = True
            for gen in N.generators:
                if gen.size > n:
                    # If the generator's size is larger than n, it must fix all points >= n
                    if any(gen(i) != i for i in range(n, gen.size)):
                        is_subgroup = False
                        break
            
            if not is_subgroup:
                h2_ok = False
            else:
                # Check if N is normal in Sn
                is_normal = True
                for g in Sn.generators:
                    for h in N.generators:
                        conj = g * h * (~g)
                        if conj not in N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h2_ok = is_normal
    except Exception:
        h2_ok = False

    # ¬Q: N is not the trivial subgroup, not A_n, and not S_n
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, N = witness
        else:
            N = witness
            n = N.degree
            
        if not isinstance(N, PermutationGroup):
            neg_q_ok = False
        else:
            order_N = N.order()
            fact_n = math.factorial(n)
            
            is_trivial = (order_N == 1)
            is_Sn = (order_N == fact_n)
            is_An = (order_N == fact_n // 2) and all(h.is_even for h in N.generators)
            
            neg_q_ok = not (is_trivial or is_An or is_Sn)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer with n >= 5",
    "H_2: N is a normal subgroup of S_n",
    "¬Q: N is not the trivial subgroup, not A_n, and not S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2