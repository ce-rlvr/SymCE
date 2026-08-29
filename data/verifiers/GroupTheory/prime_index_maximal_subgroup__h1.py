import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(H.is_subgroup(G))
    except Exception:
        try:
            h1 = all(g in G for g in H.generators)
        except Exception:
            h1 = False
        
    try:
        if h1:
            index = G.order() // H.order()
            h2 = bool(sympy.ntheory.isprime(index))
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        if not h1:
            neg_q = False
        elif H.order() == G.order():
            # A maximal subgroup must be a proper subgroup
            neg_q = True
        else:
            is_maximal = True
            elements = G.elements if hasattr(G, 'elements') else G.generate()
            for g in elements:
                if g not in H:
                    gens = list(H.generators) + [g]
                    K = sympy.combinatorics.PermutationGroup(gens)
                    if K.order() < G.order():
                        is_maximal = False
                        break
            neg_q = not is_maximal
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The index of H in G is a prime number",
    "¬Q: H is not a maximal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2