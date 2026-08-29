import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, sigma = witness
        else:
            sigma = witness
            n = sigma.size if hasattr(sigma, 'size') else None
            
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    try:
        h2 = isinstance(sigma, Permutation)
        if h2 and isinstance(witness, tuple) and len(witness) == 2:
            h2 = sigma.size <= n
    except Exception:
        h2 = False

    try:
        # P: sigma is an involution (its square is the identity)
        sq = sigma * sigma
        P = list(sq) == list(range(sq.size))
        
        # Q: disjoint cycle decomposition consists entirely of 1-cycles and 2-cycles, with at least one 2-cycle
        # Note: sympy's cyclic_form omits 1-cycles, so we just check that all present cycles have length 2
        cycles = sigma.cyclic_form
        Q = all(len(c) == 2 for c in cycles) and len(cycles) >= 1
        
        # The conclusion is P <-> Q. We want the negation to be True, so P XOR Q.
        neg_q = bool(P != Q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: sigma is a permutation in S_n",
    "¬Q: sigma is an involution XOR its disjoint cycle decomposition consists entirely of 1-cycles and 2-cycles, with at least one 2-cycle"
]

N_HYP = 2
NEG_Q_INDEX = 2