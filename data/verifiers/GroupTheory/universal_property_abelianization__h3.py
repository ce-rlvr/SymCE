import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, A, f = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(A, PermutationGroup) and A.is_abelian
    except Exception:
        h2 = False
        
    try:
        G_elems = list(G.elements)
        A_elems = list(A.elements)
        
        if isinstance(f, dict):
            h3 = set(f.keys()) == set(G_elems) and all(v in A_elems for v in f.values())
            f_dict = f
        elif callable(f):
            h3 = all(f(g) in A_elems for g in G_elems)
            f_dict = {g: f(g) for g in G_elems}
        else:
            h3 = False
            f_dict = {}
    except Exception:
        h3 = False
        f_dict = {}

    try:
        if not h3:
            neg_q = False
        else:
            is_hom = True
            for x in G_elems:
                for y in G_elems:
                    if f_dict[x * y] != f_dict[x] * f_dict[y]:
                        is_hom = False
                        break
                if not is_hom:
                    break
            neg_q = not is_hom
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: A is an abelian group",
    "H_3: f is a function from G to A",
    "¬Q: f is not a homomorphism, so no such unique homomorphism f_tilde exists"
]

N_HYP = 3
NEG_Q_INDEX = 3