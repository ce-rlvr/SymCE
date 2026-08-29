import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
        G = witness['G']
        H = witness['H']
        f = witness['f']
        A = witness['A']
        B = witness['B']
    except Exception:
        return [False, False, False, False]

    def apply_f(x):
        if isinstance(f, dict):
            return f[x]
        return f(x)

    # H1: G and H are groups, and A, B are subsets of G
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
        if h1:
            elements_G = list(G.generate())
            h1 = all(a in elements_G for a in A) and all(b in elements_G for b in B)
    except Exception:
        h1 = False

    # H2: f: G -> H is a group homomorphism
    try:
        elements_G = list(G.generate())
        elements_H = list(H.generate())
        h2 = True
        for g in elements_G:
            if isinstance(f, dict) and g not in f:
                h2 = False
                break
            if apply_f(g) not in elements_H:
                h2 = False
                break
        if h2:
            for g1 in elements_G:
                for g2 in elements_G:
                    if apply_f(g1 * g2) != apply_f(g1) * apply_f(g2):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: ker(f) is a subset of A
    try:
        elements_G = list(G.generate())
        elements_H = list(H.generate())
        id_H = None
        for h in elements_H:
            if h * h == h:
                id_H = h
                break
        ker_f = [g for g in elements_G if apply_f(g) == id_H]
        h3 = all(k in A for k in ker_f)
    except Exception:
        h3 = False

    # neg_Q: f(A \cap B) != f(A) \cap f(B)
    try:
        A_set = set(A)
        B_set = set(B)
        A_cap_B = A_set.intersection(B_set)
        
        f_A = set(apply_f(a) for a in A_set)
        f_B = set(apply_f(b) for b in B_set)
        f_A_cap_B = set(apply_f(x) for x in A_cap_B)
        
        f_A_cap_f_B = f_A.intersection(f_B)
        
        neg_q = f_A_cap_B != f_A_cap_f_B
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G -> H is a group homomorphism",
    "H_3: ker(f) is a subset of A",
    "¬Q: f(A ∩ B) != f(A) ∩ f(B)"
]

N_HYP = 3
NEG_Q_INDEX = 3