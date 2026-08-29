import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import factorint

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_sylow_subgroup(G, H):
    try:
        if not isinstance(H, PermutationGroup):
            return False
        # Check if H is a subgroup of G
        for g in H.generators:
            if g not in G:
                return False
        oH = H.order()
        oG = G.order()
        if oG % oH != 0:
            return False
        if oH == 1:
            return True
        factors = factorint(oH)
        if len(factors) != 1:
            return False
        p = list(factors.keys())[0]
        # Check if it is the maximal p-power dividing the order of G
        if (oG // oH) % p == 0:
            return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, P, Q = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: P is a Sylow p-subgroup of G
    try:
        h2 = is_sylow_subgroup(G, P)
    except Exception:
        h2 = False
        
    # H_3: Q is a Sylow p-subgroup of G
    try:
        h3 = is_sylow_subgroup(G, Q)
    except Exception:
        h3 = False
        
    # ¬Q: There does NOT exist g in G such that Q = gPg^(-1)
    try:
        if not (isinstance(G, PermutationGroup) and isinstance(P, PermutationGroup) and isinstance(Q, PermutationGroup)):
            neg_q = False
        elif P.order() != Q.order():
            # If they have different orders, they cannot be conjugate
            neg_q = True
        else:
            is_conj = False
            for g in G.generate():
                subset = True
                for gen in P.generators:
                    conj = g * gen * ~g
                    if conj not in Q:
                        subset = False
                        break
                if subset:
                    is_conj = True
                    break
            neg_q = not is_conj
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: Q is a Sylow p-subgroup of G",
    "¬Q: P and Q are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3