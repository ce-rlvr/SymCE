import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import isprime, factorint
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
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        N, H, p = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        if isinstance(N, list):
            N = PermutationGroup(N)
        if isinstance(H, list):
            H = PermutationGroup(H)
    except Exception:
        pass

    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: N is an abelian p-group
    try:
        if not N.is_abelian:
            h2 = False
        else:
            order_N = N.order()
            if order_N == 1:
                h2 = True
            else:
                factors = factorint(order_N)
                h2 = (list(factors.keys()) == [p])
    except Exception:
        h2 = False

    # H_3: The order of H is coprime to p
    try:
        h3 = math.gcd(H.order(), int(p)) == 1
    except Exception:
        h3 = False

    # ¬Q: N is NOT the internal direct product of C_N(H) and [N, H]
    try:
        N_elements = list(N.generate())
        H_elements = list(H.generate())
        
        # Compute C_N(H)
        C_N_H = []
        for n in N_elements:
            if all(n * h == h * n for h in H_elements):
                C_N_H.append(n)
                
        # Compute generators for [N, H]
        commutators = []
        for n in N_elements:
            for h in H_elements:
                commutators.append(~n * ~h * n * h)
                
        if not commutators:
            comm_NH = PermutationGroup([N_elements[0] * ~N_elements[0]])
        else:
            comm_NH = PermutationGroup(commutators)
            
        # Check if [N, H] is a subgroup of N
        comm_in_N = True
        for g in commutators:
            try:
                if not N.contains(g):
                    comm_in_N = False
                    break
            except Exception:
                comm_in_N = False
                break
                
        # Check intersection C_N(H) ∩ [N, H]
        intersection_size = 0
        for g in C_N_H:
            try:
                if comm_NH.contains(g):
                    intersection_size += 1
            except Exception:
                pass
                
        # For an internal direct product of abelian N:
        # 1. Both are subgroups of N (comm_in_N ensures [N, H] <= N, C_N(H) is trivially <= N)
        # 2. Trivial intersection
        # 3. Their product generates N (sizes multiply to |N|)
        is_direct_product = comm_in_N and (intersection_size == 1) and (len(C_N_H) * comm_NH.order() == N.order())
        
        neg_q = not is_direct_product
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: N is an abelian p-group",
    "H_3: The order of H is coprime to p",
    "¬Q: N is not the internal direct product of C_N(H) and the mixed commutator subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3