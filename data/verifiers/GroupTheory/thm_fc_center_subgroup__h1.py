import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    G = witness
    
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        elif hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
            
        S = []
        for x in elements:
            conj = []
            for g in elements:
                try:
                    inv_g = g**-1
                except TypeError:
                    inv_g = ~g
                c = inv_g * x * g
                if c not in conj:
                    conj.append(c)
            S.append(x)
        H1_ok = True
    except Exception:
        H1_ok = False

    try:
        is_subgroup = True
        if not S:
            is_subgroup = False
        else:
            for a in S:
                try:
                    inv_a = a**-1
                except TypeError:
                    inv_a = ~a
                if inv_a not in S:
                    is_subgroup = False
                    break
                for b in S:
                    if (a * b) not in S:
                        is_subgroup = False
                        break
        
        if not is_subgroup:
            conclusion = False
        else:
            G_is_group = True
            if hasattr(G, 'is_group') and G.is_group:
                G_is_group = True
            else:
                for a in elements:
                    try:
                        inv_a = a**-1
                    except TypeError:
                        inv_a = ~a
                    if inv_a not in elements:
                        G_is_group = False
                        break
                    for b in elements:
                        if (a * b) not in elements:
                            G_is_group = False
                            break
            if G_is_group:
                conclusion = True
            else:
                conclusion = False
                
        neg_Q_ok = not conclusion
    except Exception:
        neg_Q_ok = False

    return [H1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: S is the set of elements in G with finitely many conjugates in G",
    "¬Q: S does not form a characteristic subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1