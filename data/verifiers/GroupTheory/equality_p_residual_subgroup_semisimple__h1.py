import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.ntheory import isprime
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, p = witness
    except Exception:
        return [False, False]
    
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # ¬Q: O^p(G) is not equal to G
    try:
        gens = []
        for g in G.generate():
            if math.gcd(g.order(), p) == 1:
                gens.append(g)
        
        if not gens:
            opg_order = 1
        else:
            OpG = PermutationGroup(*gens)
            opg_order = OpG.order()
            
        neg_q = bool(opg_order != G.order())
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: O^p(G) is not equal to G"
]

N_HYP = 1
NEG_Q_INDEX = 1