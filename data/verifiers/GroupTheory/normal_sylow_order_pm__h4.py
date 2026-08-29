import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False, False, False]
        G, p, m = witness
    except Exception:
        return [False, False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False
        
    # H_3: m is a positive integer
    try:
        h3 = bool(isinstance(m, (int, sympy.Integer)) and m > 0)
    except Exception:
        h3 = False
        
    # H_4: p > m
    try:
        h4 = bool(p > m)
    except Exception:
        h4 = False
        
    # ¬Q: The Sylow p-subgroup of G is not a normal subgroup of G
    try:
        H = G.sylow_subgroup(p)
        if hasattr(G, 'is_normal'):
            is_norm = G.is_normal(H)
        else:
            is_norm = True
            for g in G.generators:
                for h in H.generators:
                    conj = g * h * (~g)
                    if conj not in H:
                        is_norm = False
                        break
                if not is_norm:
                    break
        neg_q = not is_norm
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: m is a positive integer",
    "H_4: p > m",
    "¬Q: The Sylow p-subgroup of G is not a normal subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4