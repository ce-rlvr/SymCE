import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
    "H_1: n is an integer strictly greater than 1",
    "H_2: a and b are in G and satisfy the relations R",
    "¬Q: G is not isomorphic to the dicyclic group Dic_n of order 4n"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            n, G, a, b = witness
        elif len(witness) == 3:
            n, a, b = witness
            G = PermutationGroup(a, b)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: n is an integer strictly greater than 1
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 1
    except Exception:
        h1 = False

    # H_2: a and b are in G and satisfy the relations R
    try:
        if not (a in G and b in G):
            h2 = False
        else:
            id_G = a**0
            rel1 = (a**(2*n) == id_G)
            rel2 = (b**2 == a**n)
            rel3 = (b**-1 * a * b == a**-1)
            h2 = bool(rel1 and rel2 and rel3)
    except Exception:
        h2 = False

    # ¬Q: G is not isomorphic to the dicyclic group Dic_n of order 4n
    try:
        if G.order() != 4 * n:
            is_iso = False
        else:
            a_perm = []
            for i in range(4*n):
                if i < 2*n:
                    a_perm.append((i + 1) % (2*n))
                else:
                    a_perm.append(2*n + (i - 2*n + 1) % (2*n))
            
            b_perm = []
            for i in range(4*n):
                if i < 2*n:
                    b_perm.append(2*n + (-i) % (2*n))
                else:
                    b_perm.append((n - (i - 2*n)) % (2*n))
            
            Dic_n = PermutationGroup(Permutation(a_perm), Permutation(b_perm))
            is_iso = G.is_isomorphic(Dic_n)
            
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]