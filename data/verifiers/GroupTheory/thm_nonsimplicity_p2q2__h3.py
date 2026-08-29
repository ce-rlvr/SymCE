import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy import isprime, oo

# Top-level setup: named object bindings
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

def conditions(witness):
    try:
        # The witness must provide the group G and the two primes p, q
        if len(witness) != 3:
            return [False, False, False]
        G, p, q = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite group
    try:
        o = G.order()
        h1_ok = (o != oo) and (o > 0)
    except Exception:
        h1_ok = False

    # H_2: p and q are distinct prime numbers
    try:
        h2_ok = isprime(p) and isprime(q) and (p != q)
    except Exception:
        h2_ok = False

    # ¬Q: G is a simple group (negation of "G is not a simple group")
    try:
        neg_q_ok = False
        if h1_ok:
            o = G.order()
            if o > 1:
                if isprime(o):
                    neg_q_ok = True
                elif isinstance(G, AlternatingGroup) and getattr(G, 'degree', 0) >= 5:
                    neg_q_ok = True
                elif o == 60 and not getattr(G, 'is_solvable', True):
                    neg_q_ok = True
                elif hasattr(G, 'is_simple'):
                    if callable(G.is_simple):
                        neg_q_ok = G.is_simple()
                    else:
                        neg_q_ok = bool(G.is_simple)
                elif hasattr(G, 'normal_subgroups') and callable(G.normal_subgroups):
                    neg_q_ok = len(G.normal_subgroups()) == 2
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p and q are distinct prime numbers",
    "¬Q: G is a simple group"
]

N_HYP = 2
NEG_Q_INDEX = 2