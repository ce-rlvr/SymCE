import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) != 2:
                return [False, False]
            G, p = witness
            if not isinstance(p, (int, sympy.Integer)):
                return [False, False]
            if not isprime(p):
                return [False, False]
        else:
            G = witness
            p = None

        if not isinstance(G, PermutationGroup):
            return [False, False]

        h1 = True

        D = G.derived_subgroup()
        idx = G.order() // D.order()

        if p is not None:
            q_holds = (idx % p == 0)
        else:
            q_holds = (idx > 1)

        neg_q = not q_holds

        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "not Q: There is no intermediate field E with E/K Galois and degree E over K is p"
]

N_HYP = 1
NEG_Q_INDEX = 1