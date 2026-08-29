import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness) -> list[bool]:
    try:
        G, p = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(p, int)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(isprime(p))
    except Exception:
        h2_ok = False

    try:
        h3_ok = bool(G.order() % p == 0)
    except Exception:
        h3_ok = False

    try:
        P = G.sylow_subgroup(p)
        P_elements = list(P.generate_dimino())
        conjugates = set()
        for g in G.generate_dimino():
            conj = frozenset([g * x * (~g) for x in P_elements])
            conjugates.add(conj)
        n_p = len(conjugates)
        
        q_holds = (G.order() % n_p == 0) and (n_p % p == 1)
        neg_q_ok = not q_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: p divides the order of G",
    "¬Q: n_p does not divide the order of G or n_p is not 1 mod p"
]

N_HYP = 3
NEG_Q_INDEX = 3