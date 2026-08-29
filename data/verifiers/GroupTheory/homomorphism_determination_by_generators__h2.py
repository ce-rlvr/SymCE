import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def eval_map(m, x):
    if isinstance(m, dict):
        return m[x]
    return m(x)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            S = witness.get('S')
            f = witness.get('f')
            g = witness.get('g')
        else:
            G, H, S, f, g = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: f and g are group homomorphisms from G to H
    try:
        h2 = True
        if h1:
            G_elems = list(G.elements)
            for x in G_elems:
                fx = eval_map(f, x)
                gx = eval_map(g, x)
                if fx not in H or gx not in H:
                    h2 = False
                    break
            if h2:
                for x in G_elems:
                    for y in G_elems:
                        xy = x * y
                        fxy = eval_map(f, xy)
                        fx_fy = eval_map(f, x) * eval_map(f, y)
                        if fxy != fx_fy:
                            h2 = False
                            break
                        gxy = eval_map(g, xy)
                        gx_gy = eval_map(g, x) * eval_map(g, y)
                        if gxy != gx_gy:
                            h2 = False
                            break
                    if not h2:
                        break
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: For every s \in S, f(s) = g(s)
    try:
        h3 = True
        if h1:
            G_elems = list(G.elements)
            for s in S:
                if s not in G_elems:
                    h3 = False
                    break
                if eval_map(f, s) != eval_map(g, s):
                    h3 = False
                    break
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: f(x) != g(x) for some x \in G
    try:
        neg_q = False
        if h1:
            G_elems = list(G.elements)
            for x in G_elems:
                if eval_map(f, x) != eval_map(g, x):
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f and g are group homomorphisms from G to H",
    "H_3: For every s in S, f(s) = g(s)",
    "¬Q: There exists x in G such that f(x) != g(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3