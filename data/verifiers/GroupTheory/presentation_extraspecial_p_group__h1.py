import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.ntheory

# Standard named groups
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

def admits_presentation(G, p):
    if len(G.elements) != p**3:
        return False
    elements = list(G.elements)
    id_el = G.identity
    for x in elements:
        if x**p != id_el: continue
        for y in elements:
            if y**p != id_el: continue
            # [x, y] = x^-1 y^-1 x y
            z = x**-1 * y**-1 * x * y
            if z == id_el: continue
            if z**p != id_el: continue
            if x*z != z*x: continue
            if y*z != z*y: continue
            # Since G has order p^3 and x, y do not commute, 
            # they must generate the whole group G.
            return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            factors = sympy.ntheory.factorint(len(G.elements))
            if len(factors) == 1:
                p = list(factors.keys())[0]
            else:
                return [False, False]
    except Exception:
        return [False, False]

    try:
        is_p_grp = len(G.elements) == p**3
        exp_ok = all(g**p == G.identity for g in G.elements)
        center = [g for g in G.elements if all(g*h == h*g for h in G.elements)]
        center_ok = len(center) == p
        h1 = is_p_grp and exp_ok and center_ok
    except Exception:
        h1 = False

    try:
        neg_q = not admits_presentation(G, p)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the extraspecial p-group of order p^3 and exponent p",
    "¬Q: G does not admit the presentation"
]

N_HYP = 1
NEG_Q_INDEX = 1