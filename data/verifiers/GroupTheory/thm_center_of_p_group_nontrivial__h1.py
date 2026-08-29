import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
    # Unpack witness if it's provided as a tuple (G, p) or (G, p, n)
    if isinstance(witness, tuple):
        if len(witness) == 3:
            G, p, n = witness
        elif len(witness) == 2:
            G, p = witness
            n = None
        else:
            G = witness
            p = None
            n = None
    else:
        G = witness
        p = None
        n = None

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: The order of G is p^n for some integer n >= 1
    try:
        if h1_ok:
            order = G.order()
            if p is not None and n is not None:
                try:
                    h2_ok = (int(p)**int(n) == order) and int(n) >= 1
                except Exception:
                    h2_ok = False
            elif p is not None:
                try:
                    p_val = int(p)
                    h2_ok = False
                    if p_val != 0:
                        n_val = 1
                        while abs(p_val)**n_val <= order:
                            if p_val**n_val == order:
                                h2_ok = True
                                break
                            if abs(p_val) == 1:
                                break
                            n_val += 1
                except Exception:
                    h2_ok = False
            else:
                # If p is not specified, we can always choose p = order and n = 1
                # since order >= 1 for any finite group.
                h2_ok = True
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The center of G, Z(G), contains at most one element (negation of strictly more than one)
    try:
        if h1_ok:
            # G.center() returns a list of permutations in the center
            neg_q_ok = len(G.center()) <= 1
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is p^n for some integer n >= 1",
    "¬Q: The center of G, Z(G), contains at most one element"
]

N_HYP = 2
NEG_Q_INDEX = 2