import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x_1, ..., x_k are representatives of the distinct conjugacy classes of G of size greater than 1",
    "¬Q: |G| != |Z(G)| + sum_{i=1}^k (G : C_G(x_i))"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            G = witness[0]
            if len(witness) == 2 and isinstance(witness[1], (list, tuple, set)):
                X = list(witness[1])
            else:
                X = list(witness[1:])
        else:
            G = witness
            X = []
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            try:
                elements = list(G.generate())
            except Exception:
                elements = list(G.elements)
    except Exception:
        h1 = False

    # H_2: x_1, ..., x_k are representatives of the distinct conjugacy classes of G of size greater than 1
    try:
        if not h1:
            h2 = False
        else:
            classes = []
            seen = set()
            for x in elements:
                if x in seen:
                    continue
                cclass = set()
                for g in elements:
                    cclass.add(g * x * ~g)
                classes.append(cclass)
                seen.update(cclass)
            
            classes_gt_1 = [c for c in classes if len(c) > 1]
            
            matched_classes = set()
            h2 = True
            for x in X:
                found = False
                for i, c in enumerate(classes_gt_1):
                    if x in c:
                        matched_classes.add(i)
                        found = True
                        break
                if not found:
                    h2 = False
                    break
            if h2:
                if len(matched_classes) != len(classes_gt_1):
                    h2 = False
    except Exception:
        h2 = False

    # ¬Q: |G| != |Z(G)| + sum_{i=1}^k (G : C_G(x_i))
    try:
        if not h1:
            neg_q = False
        else:
            Z_G = [x for x in elements if all(g * x == x * g for g in elements)]
            len_Z_G = len(Z_G)
            
            sum_index = 0
            for x in X:
                c_g_x_size = sum(1 for g in elements if g * x == x * g)
                index = len(elements) // c_g_x_size
                sum_index += index
                
            q = (len(elements) == len_Z_G + sum_index)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]