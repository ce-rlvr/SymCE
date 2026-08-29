import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: P \\cap Z(G) is not the unique Sylow p-subgroup of Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)):
            return [False, False, False]
        if len(witness) == 3:
            G, P, p = witness
        elif len(witness) == 2:
            G, P = witness
            p = None
        else:
            return [False, False, False]
            
        if isinstance(P, list):
            P = PermutationGroup(P)
            
        if p is None:
            if not isinstance(P, PermutationGroup):
                return [False, False, False]
            order_P = P.order()
            factors = sympy.factorint(order_P)
            if len(factors) == 1:
                p = list(factors.keys())[0]
            elif order_P == 1:
                p = 2
                try:
                    while G.order() % p == 0:
                        p = sympy.nextprime(p)
                except Exception:
                    pass
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        h2 = False
        if h1 and isinstance(P, PermutationGroup) and all(g in G for g in P.generators) and sympy.isprime(p):
            order_G = G.order()
            order_P = P.order()
            k = 0
            temp = order_G
            while temp % p == 0:
                k += 1
                temp //= p
            if order_P == p**k:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: P \cap Z(G) is not the unique Sylow p-subgroup of Z(G)
    try:
        neg_q = False
        if h1 and h2:
            Z = G.center()
            order_Z = Z.order()
            m = 0
            temp = order_Z
            while temp % p == 0:
                m += 1
                temp //= p
            expected_order = p**m
            
            try:
                Z_elems = list(Z.generate())
            except AttributeError:
                Z_elems = list(Z.elements)
                
            actual_order = sum(1 for g in Z_elems if g in P)
            
            if actual_order != expected_order:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]