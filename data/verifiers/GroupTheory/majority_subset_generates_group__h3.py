import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        G, S = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: S is a subset of G
    try:
        h2 = isinstance(S, (list, set, tuple)) and all(s in G for s in S)
    except Exception:
        h2 = False
        
    # ¬Q: There exists g in G such that g cannot be written as xy for x, y in S
    try:
        products = set()
        for x in S:
            for y in S:
                products.add(x * y)
                
        neg_q = False
        elements = getattr(G, 'elements', None)
        if elements is None:
            elements = list(G.generate())
            
        for g in elements:
            if g not in products:
                neg_q = True
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: S is a subset of G",
    "¬Q: There exists g in G such that g cannot be written as xy for x, y in S"
]

N_HYP = 2
NEG_Q_INDEX = 2