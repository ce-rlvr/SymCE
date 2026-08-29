import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

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
        G, a, k = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(hasattr(G, 'is_cyclic') and G.is_cyclic and (a in G))
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(k, (int, sympy.Integer))
    except Exception:
        h2 = False
        
    try:
        n = G.order()
        a_k = a**k
        # In a finite group, an element generates the group iff its order equals the group's order
        a_k_generates_G = (a_k.order() == n)
        gcd_condition = (math.gcd(int(k), int(n)) == 1)
        
        # The conclusion states they are equivalent. We want the negation (they are not equivalent).
        neg_q = bool(a_k_generates_G != gcd_condition)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group and a is an element of G",
    "H_2: k is an integer",
    "¬Q: a^k generates G if and only if gcd(k, n) = 1 is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2