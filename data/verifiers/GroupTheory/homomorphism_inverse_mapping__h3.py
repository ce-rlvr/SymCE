import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def apply_f(f, a):
    if isinstance(f, dict):
        return f[a]
    else:
        return f(a)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    The witness can be either (G, H, f) or (G, H, f, x).
    """
    try:
        if len(witness) == 3:
            G, H, f = witness
            x_val = None
        elif len(witness) == 4:
            G, H, f, x_val = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = hasattr(G, 'elements') and hasattr(H, 'elements')
    except Exception:
        h1 = False

    # H_2: f: G \to H is a group homomorphism
    try:
        h2 = False
        if h1:
            h2 = True
            for a in G.elements:
                fa = apply_f(f, a)
                if fa not in H.elements:
                    h2 = False
                    break
                for b in G.elements:
                    fb = apply_f(f, b)
                    fab = apply_f(f, a * b)
                    if fab != fa * fb:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: f(x^{-1}) != (f(x))^{-1}
    try:
        neg_q = False
        if h1:
            if x_val is not None:
                if x_val in G.elements:
                    x_inv = x_val ** -1
                    fx = apply_f(f, x_val)
                    fx_inv = apply_f(f, x_inv)
                    if fx_inv != fx ** -1:
                        neg_q = True
            else:
                for x in G.elements:
                    x_inv = x ** -1
                    fx = apply_f(f, x)
                    fx_inv = apply_f(f, x_inv)
                    if fx_inv != fx ** -1:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G \\to H is a group homomorphism",
    "¬Q: f(x^{-1}) != (f(x))^{-1}"
]

N_HYP = 2
NEG_Q_INDEX = 2