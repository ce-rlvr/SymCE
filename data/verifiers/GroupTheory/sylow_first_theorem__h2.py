import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup
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
        G, p, n, m = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = bool(isinstance(G, PermutationGroup) and G.order() > 0)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False
        
    # H_3: n is an integer greater than or equal to 1
    try:
        h3 = bool(isinstance(n, (int, sympy.Integer)) and n >= 1)
    except Exception:
        h3 = False
        
    # H_4: p does not divide m
    try:
        h4 = bool(isinstance(m, (int, sympy.Integer)) and (m % p != 0))
    except Exception:
        h4 = False
        
    # ¬Q: G does not contain a subgroup of order p^n
    # By Sylow's theorems and properties of p-groups, a finite group contains a 
    # subgroup of order p^n if and only if p^n divides the order of the group.
    try:
        neg_q = bool((G.order() % (p**n)) != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: n is an integer greater than or equal to 1",
    "H_4: p does not divide m",
    "¬Q: G does not contain a subgroup of order p^n"
]

N_HYP = 4
NEG_Q_INDEX = 4