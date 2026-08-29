import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime

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
        G, p, q, n = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p and q are distinct prime numbers
    try:
        h2 = bool(isprime(p) and isprime(q) and p != q)
    except Exception:
        h2 = False
        
    # H_3: n is a positive integer such that p^n < q
    try:
        h3 = bool(isinstance(n, (int, sympy.Integer)) and n > 0 and (p**n) < q)
    except Exception:
        h3 = False
        
    # ¬Q: The Sylow q-subgroup of G is not a normal subgroup of G
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            try:
                H = G.sylow_subgroup(q)
            except Exception:
                H = None
                
            if H is None:
                is_norm = True
            else:
                is_norm = True
                for g in G.generators:
                    g_inv = ~g
                    for h in H.generators:
                        conj = g * h * g_inv
                        if not H.contains(conj):
                            is_norm = False
                            break
                    if not is_norm:
                        break
            neg_q = not is_norm
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p and q are distinct prime numbers",
    "H_3: n is a positive integer such that p^n < q",
    "¬Q: The Sylow q-subgroup of G is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3