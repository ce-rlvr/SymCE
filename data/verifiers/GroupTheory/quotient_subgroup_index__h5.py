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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False] * 5
        
    # H1: G is a group
    try:
        if hasattr(G, 'is_group'):
            h1 = bool(G.is_group)
        else:
            h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h2 = False
        
    # H3: H is a subgroup of G
    try:
        h3 = bool(H.is_subgroup(G))
    except Exception:
        h3 = False
        
    # H4: N is a subset of H
    try:
        h4 = bool(N.is_subgroup(H))
    except Exception:
        h4 = False
        
    # neg_Q: The index of the quotient subgroup H/N in the quotient group G/N is equal to the index of H in G
    try:
        order_G = G.order()
        order_H = H.order()
        order_N = N.order()
        
        index_G_H = sympy.Rational(order_G, order_H)
        order_GN = sympy.Rational(order_G, order_N)
        order_HN = sympy.Rational(order_H, order_N)
        index_GN_HN = sympy.Rational(order_GN, order_HN)
        
        q = (index_GN_HN == index_G_H)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "H_4: N is a subset of H",
    "¬Q: The index of the quotient subgroup H/N in the quotient group G/N is not equal to the index of H in G"
]

N_HYP = 4
NEG_Q_INDEX = 4