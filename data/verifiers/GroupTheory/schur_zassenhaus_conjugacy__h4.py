import math
import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: G is a finite group, and N, H1, H2 are subgroups of G",
    "H_2: N is a normal subgroup of G",
    "H_3: The order of N and the index of N in G are coprime",
    "¬Q: H1 and H2 are not conjugate subgroups in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        G, N, H1, H2 = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a finite group, and N, H1, H2 are subgroups
    try:
        h1_ok = (isinstance(G, PermutationGroup) and 
                 isinstance(N, PermutationGroup) and 
                 isinstance(H1, PermutationGroup) and 
                 isinstance(H2, PermutationGroup))
        if h1_ok:
            for h in N.generators:
                if h not in G:
                    h1_ok = False
            for h in H1.generators:
                if h not in G:
                    h1_ok = False
            for h in H2.generators:
                if h not in G:
                    h1_ok = False
    except Exception:
        h1_ok = False

    # H2: N is a normal subgroup of G
    try:
        h2_ok = False
        if h1_ok:
            h2_ok = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        h2_ok = False
                        break
                if not h2_ok:
                    break
    except Exception:
        h2_ok = False

    # H3: order of N and index of N in G are coprime
    try:
        h3_ok = False
        if h1_ok:
            order_N = N.order()
            order_G = G.order()
            if order_G % order_N == 0:
                index = order_G // order_N
                h3_ok = (math.gcd(order_N, index) == 1)
    except Exception:
        h3_ok = False

    # neg_Q: H1 and H2 are NOT conjugate subgroups in G
    try:
        neg_q = False
        if h1_ok:
            if H1.order() != H2.order():
                neg_q = True
            else:
                try:
                    elements = list(G.elements)
                except AttributeError:
                    elements = list(G.generate())
                
                are_conj = False
                for g in elements:
                    is_conj = True
                    for h in H1.generators:
                        if (g * h * ~g) not in H2:
                            is_conj = False
                            break
                    if is_conj:
                        are_conj = True
                        break
                neg_q = not are_conj
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]