import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        G, p = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    try:
        order = G.order()
        h2 = (order % p == 0)
    except Exception:
        h2 = False
        
    try:
        P = G.sylow_subgroup(p)
        P_elements = set(P.generate())
        conjugates = set()
        for g in G.generate():
            conj = frozenset([g * x * ~g for x in P_elements])
            conjugates.add(conj)
        n_p = len(conjugates)
        neg_q = (n_p != 1)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p divides the order of G",
    "¬Q: G does not have exactly one Sylow p-subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2
