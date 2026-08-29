import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.ntheory import totient

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            n = witness['n']
        else:
            G, n = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(n, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        h2 = bool(G.is_cyclic)
    except Exception:
        h2 = False

    try:
        if getattr(G, 'is_cyclic', False):
            gen_count = totient(G.order())
        else:
            order_G = G.order()
            gen_count = sum(1 for g in G.elements if g.order() == order_G)
        neg_q = bool(gen_count != totient(n))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a cyclic group",
    "¬Q: The number of generators of G is not equal to phi(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2