import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(G.degree, int)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(G.is_transitive)
    except Exception:
        h2_ok = False

    try:
        h3_ok = bool(isinstance(x, int) and 0 <= x < G.degree)
    except Exception:
        h3_ok = False

    try:
        h4_ok = bool(isinstance(y, int) and 0 <= y < G.degree)
    except Exception:
        h4_ok = False

    try:
        stab_x = G.stabilizer(x)
        stab_y = G.stabilizer(y)
        
        stab_x_elems = set(stab_x.generate_dimino())
        stab_y_elems = set(stab_y.generate_dimino())
        
        neg_q_ok = True
        for g in G.generate_dimino():
            g_inv = ~g
            conj_elems = {g * h * g_inv for h in stab_x_elems}
            if conj_elems == stab_y_elems:
                neg_q_ok = False
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts transitively on X",
    "H_3: x is an element of X",
    "H_4: y is an element of X",
    "¬Q: For all g in G, Stab_G(y) != g * Stab_G(x) * g^{-1}"
]

N_HYP = 4
NEG_Q_INDEX = 4