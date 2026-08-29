import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup, Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            P = witness.get('P')
            N = witness.get('N')
            p = witness.get('p')
        else:
            G, P, N, p = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group (and N is a subgroup, p is prime)
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(N, PermutationGroup) and 
              isprime(p) and 
              all(g in G for g in N.generators))
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        h2 = False
        if isinstance(P, PermutationGroup) and all(g in G for g in P.generators):
            order_G = G.order()
            order_P = P.order()
            
            is_p_group = True
            temp = order_P
            while temp > 1:
                if temp % p != 0:
                    is_p_group = False
                    break
                temp //= p
                
            if is_p_group:
                index = order_G // order_P
                if index % p != 0:
                    h2 = True
    except Exception:
        h2 = False

    # neg_Q: N is not a subgroup of P
    try:
        is_subgroup = all(g in P for g in N.generators)
        neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group (and N is a subgroup, p is prime)",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: N is not a subgroup of P"
]

N_HYP = 2
NEG_Q_INDEX = 2