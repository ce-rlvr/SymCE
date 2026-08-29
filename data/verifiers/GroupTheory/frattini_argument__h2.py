import sympy
import sympy.ntheory
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        G, N, p, P = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = sympy.ntheory.isprime(p)
    except Exception:
        h2 = False

    # H3: P is a Sylow p-subgroup of N
    try:
        if not (isinstance(N, PermutationGroup) and isinstance(P, PermutationGroup)):
            h3 = False
        elif type(p) != int and not isinstance(p, sympy.Integer):
            h3 = False
        elif p <= 1:
            h3 = False
        else:
            G_elements = set(G.generate())
            if not all(g in G_elements for g in N.generators):
                h3 = False
            else:
                N_elements = set(N.generate())
                if not all(g in N_elements for g in P.generators):
                    h3 = False
                else:
                    order_N = N.order()
                    order_P = P.order()
                    
                    k = 0
                    temp = order_N
                    while temp > 0 and temp % p == 0:
                        k += 1
                        temp //= p
                    
                    h3 = (order_P == p ** k)
    except Exception:
        h3 = False

    # neg_Q: G != N * N_G(P)
    try:
        P_elements = set(P.generate())
        P_gens = P.generators
        N_G_P_elements = []
        for g in G.generate():
            # Check if g normalizes P: g * p * g^-1 in P for all generators p of P
            if all(g * p * ~g in P_elements for p in P_gens):
                N_G_P_elements.append(g)
        
        product_set = set()
        for n in N.generate():
            for m in N_G_P_elements:
                product_set.add(n * m)
                
        neg_q = len(product_set) != G.order()
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of N",
    "¬Q: G is not the product of N and the normalizer of P in G"
]

N_HYP = 3
NEG_Q_INDEX = 3