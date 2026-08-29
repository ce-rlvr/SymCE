import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.ntheory
import math

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            p, G = witness
        else:
            G = witness
            p = G.degree
    except Exception:
        return [False] * 5

    # H1: p is a prime number
    try:
        h1 = bool(sympy.ntheory.isprime(p))
    except Exception:
        h1 = False

    # H2: G is a subgroup of S_p
    try:
        h2 = isinstance(G, PermutationGroup) and G.degree <= p
    except Exception:
        h2 = False

    # H3: G acts transitively on the set {1, 2, ..., p}
    try:
        if callable(G.is_transitive):
            is_trans = G.is_transitive()
        else:
            is_trans = G.is_transitive
        h3 = bool(is_trans) and G.degree == p
    except Exception:
        h3 = False

    # H4: G contains at least one transposition
    try:
        h4 = False
        order = G.order() if callable(G.order) else G.order
        if p >= 2 and order == math.factorial(int(p)):
            h4 = True
        else:
            def is_transposition(g):
                try:
                    arr = g.array_form
                    moved = sum(1 for i, v in enumerate(arr) if i != v)
                    return moved == 2
                except Exception:
                    return False

            for g in G.generators:
                if is_transposition(g):
                    h4 = True
                    break
            
            if not h4 and order <= 10000:
                for g in G.elements:
                    if is_transposition(g):
                        h4 = True
                        break
    except Exception:
        h4 = False

    # neg_Q: G is not equal to S_p
    try:
        order = G.order() if callable(G.order) else G.order
        neg_q = order != math.factorial(int(p))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a subgroup of S_p",
    "H_3: G acts transitively on the set {1, 2, ..., p}",
    "H_4: G contains at least one transposition",
    "¬Q: G is not equal to S_p"
]

N_HYP = 4
NEG_Q_INDEX = 4