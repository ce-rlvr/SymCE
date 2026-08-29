import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, H, f = witness
            C_provided = None
        elif len(witness) == 4:
            G, H, f, C_provided = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    f_map = None
    # H2: f is a group homomorphism from G to H
    try:
        if not h1:
            h2 = False
        else:
            G_elems = list(G.elements)
            H_elems = list(H.elements)
            
            if callable(f):
                f_map = {x: f(x) for x in G_elems}
            elif hasattr(f, 'apply'):
                f_map = {x: f.apply(x) for x in G_elems}
            elif isinstance(f, dict):
                f_map = f
            elif isinstance(f, (list, tuple, set)):
                f_map = dict(f)
            else:
                f_map = None
                
            if f_map is None:
                h2 = False
            elif set(f_map.keys()) != set(G_elems):
                h2 = False
            elif not set(f_map.values()).issubset(set(H_elems)):
                h2 = False
            else:
                h2 = True
                for x in G_elems:
                    for y in G_elems:
                        if f_map[x * y] != f_map[x] * f_map[y]:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H3: C_H(f(G)) is the centralizer of the subgroup f(G) in H
    try:
        if not h1 or f_map is None:
            h3 = False
        else:
            G_elems = list(G.elements)
            H_elems = list(H.elements)
            f_G = set(f_map.values())
            
            C_H_fG = set()
            for h in H_elems:
                if all(h * y == y * h for y in f_G):
                    C_H_fG.add(h)
            
            if C_provided is not None:
                if isinstance(C_provided, (set, list)):
                    h3 = set(C_provided) == C_H_fG
                elif isinstance(C_provided, PermutationGroup):
                    h3 = set(C_provided.elements) == C_H_fG
                else:
                    h3 = False
            else:
                h3 = True
    except Exception:
        h3 = False

    # neg_Q: f(Z(G)) is not a subset of C_H(f(G))
    try:
        if not h1 or f_map is None:
            neg_q = False
        else:
            G_elems = list(G.elements)
            Z_G = set()
            for x in G_elems:
                if all(x * y == y * x for y in G_elems):
                    Z_G.add(x)
            
            f_Z_G = {f_map[z] for z in Z_G}
            
            if C_provided is not None and h3:
                if isinstance(C_provided, (set, list)):
                    C_to_use = set(C_provided)
                elif isinstance(C_provided, PermutationGroup):
                    C_to_use = set(C_provided.elements)
                else:
                    C_to_use = C_H_fG
            else:
                C_to_use = C_H_fG
                
            neg_q = not f_Z_G.issubset(C_to_use)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G -> H is a group homomorphism",
    "H_3: C_H(f(G)) is the centralizer of the subgroup f(G) in H",
    "¬Q: f(Z(G)) is not a subset of C_H(f(G))"
]

N_HYP = 3
NEG_Q_INDEX = 3