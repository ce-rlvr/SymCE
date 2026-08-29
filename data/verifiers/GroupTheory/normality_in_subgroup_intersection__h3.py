import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0,1)(2,3), Permutation(0,2)(1,3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h2 = False
        
    # ¬Q: N \cap H is not a normal subgroup of H
    try:
        if not isinstance(H, PermutationGroup):
            neg_q = False
        elif getattr(N, 'order', lambda: float('inf'))() > 5000 or getattr(H, 'order', lambda: float('inf'))() > 5000:
            neg_q = False
        else:
            I_el = []
            N_elements = list(N.generate())
            for g in H.generate():
                try:
                    if any(g == n for n in N_elements):
                        I_el.append(g)
                except Exception:
                    pass
            
            if not I_el:
                neg_q = False
            else:
                I = PermutationGroup(I_el)
                I_elements = list(I.generate())
                is_normal = True
                for h in H.generate():
                    for i in I_elements:
                        try:
                            conj = h * i * ~h
                            if not any(conj == i2 for i2 in I_elements):
                                is_normal = False
                                break
                        except Exception:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q = not is_normal
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: N \\cap H is not a normal subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2