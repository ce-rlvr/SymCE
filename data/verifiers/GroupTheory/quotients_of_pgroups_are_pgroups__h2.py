import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import sympy.ntheory

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
        G, N, p = witness
    except Exception:
        return [False, False, False]
    
    # H1: p is a prime number
    try:
        h1 = sympy.ntheory.isprime(p)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = True
        for n in N.generators:
            if not G.contains(n):
                h2 = False
                break
        if h2:
            for g in G.generators:
                g_inv = ~g
                for n in N.generators:
                    if not N.contains(g * n * g_inv):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False
        
    # neg_Q: G/N is NOT a p-group
    try:
        if not h2:
            neg_q = False
        else:
            quotient_order = G.order() // N.order()
            factors = sympy.ntheory.factorint(quotient_order)
            is_p_group = all(q == p for q in factors.keys())
            neg_q = not is_p_group
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: N is a normal subgroup of G",
    "¬Q: G/N is not a p-group"
]

N_HYP = 2
NEG_Q_INDEX = 2