import sympy
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        F = witness['F']
        X = witness['X']
        R = witness['R']
        A = witness['A']
        B = witness['B']
        alpha = witness['alpha']
        t_str = witness['t_str']
        perm_map = witness['perm_map']
    except (TypeError, KeyError):
        return [False, False, False, False]

    # H1: G is a group with presentation < X | R >
    try:
        h1 = isinstance(X, list) and isinstance(R, list)
        if h1:
            h1 = all(g in F.generators for g in X) and all(r.group == F for r in R)
    except Exception:
        h1 = False

    # H2: A and B are subgroups of G
    try:
        h2 = isinstance(A, list) and isinstance(B, list)
        if h2:
            h2 = all(a.group == F for a in A) and all(b.group == F for b in B)
    except Exception:
        h2 = False

    # H3: t is a new generator symbol not contained in X
    try:
        h3 = isinstance(t_str, str) and t_str not in [str(g) for g in X]
    except Exception:
        h3 = False

    # neg_Q: The presentation does not define an HNN extension of G (G does not embed)
    try:
        neg_q = False
        
        def eval_word(word, p_map):
            if not p_map:
                return None
            res = list(p_map.values())[0]**0
            for gen, exp in word.array_form:
                if gen not in p_map:
                    return None
                p = p_map[gen]
                res = res * (p**exp)
            return res

        valid_hom = True
        for r in R:
            val = eval_word(r, perm_map)
            if val is None or not val.is_Identity:
                valid_hom = False
                break
        
        if valid_hom:
            for a, alpha_a in alpha.items():
                val_a = eval_word(a, perm_map)
                if val_a is not None and not val_a.is_Identity:
                    # a is not identity in G
                    if alpha_a == F.identity:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group with presentation < X | R >",
    "H_2: A and B are subgroups of G",
    "H_3: t is a new generator symbol not contained in X",
    "¬Q: The presentation does not define an HNN extension of G (G does not embed)"
]

N_HYP = 3
NEG_Q_INDEX = 3