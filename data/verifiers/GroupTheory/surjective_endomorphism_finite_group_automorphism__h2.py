import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        G, f = witness
    except Exception:
        return [False, False]
    
    h1 = False
    f_dict = None
    elements = []
    try:
        if isinstance(G, PermutationGroup):
            elements = list(G.generate())
            if isinstance(f, dict):
                if all(g in f for g in elements) and all(f[g] in elements for g in elements):
                    is_hom = True
                    for x in elements:
                        for y in elements:
                            if f[x * y] != f[x] * f[y]:
                                is_hom = False
                                break
                        if not is_hom:
                            break
                    if is_hom:
                        h1 = True
                        f_dict = f
            elif callable(f):
                f_map = {g: f(g) for g in elements}
                if all(v in elements for v in f_map.values()):
                    is_hom = True
                    for x in elements:
                        for y in elements:
                            if f_map[x * y] != f_map[x] * f_map[y]:
                                is_hom = False
                                break
                        if not is_hom:
                            break
                    if is_hom:
                        h1 = True
                        f_dict = f_map
    except Exception:
        h1 = False

    neg_q = False
    if h1 and f_dict is not None:
        try:
            image = set(f_dict.values())
            if len(image) < len(elements):
                neg_q = True
        except Exception:
            pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group and f is an endomorphism of G",
    "¬Q: f is not an automorphism of G"
]

N_HYP = 1
NEG_Q_INDEX = 1