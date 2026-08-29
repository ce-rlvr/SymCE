import math
import sympy
from sympy import Rational, Integer
import sympy.combinatorics.named_groups
import sympy.matrices

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, g, p) where f and g are iterables of numbers
    (representing functions on a discrete measure space) and p is a number (or inf).
    """
    try:
        f, g, p = witness
    except Exception:
        return [False, False, False, False]

    try:
        f_list = list(f)
        g_list = list(g)
        h1 = (len(f_list) == len(g_list))
    except Exception:
        h1 = False

    try:
        if p == sympy.oo or p == float('inf'):
            p_val = float('inf')
        else:
            p_val = float(p)
        h2 = p_val >= 2.0
    except Exception:
        h2 = False

    try:
        if p_val == float('inf'):
            norm_g = max((abs(float(x)) for x in g_list), default=0.0)
        else:
            norm_g = sum(abs(float(x))**p_val for x in g_list)**(1.0/p_val) if p_val > 0 else float('inf')
        h3 = not math.isinf(norm_g) and not math.isnan(norm_g)
    except Exception:
        h3 = False

    try:
        def get_norm_p(vec, p_v):
            if p_v == float('inf'):
                norm = max((abs(float(x)) for x in vec), default=0.0)
                return math.pow(norm, float('inf'))
            else:
                return sum(abs(float(x))**p_v for x in vec)

        f_plus_g_half = [(float(x) + float(y)) / 2.0 for x, y in zip(f_list, g_list)]
        f_minus_g_half = [(float(x) - float(y)) / 2.0 for x, y in zip(f_list, g_list)]

        LHS = get_norm_p(f_plus_g_half, p_val) + get_norm_p(f_minus_g_half, p_val)
        RHS = 0.5 * (get_norm_p(f_list, p_val) + get_norm_p(g_list, p_val))

        if math.isinf(LHS) or math.isinf(RHS) or math.isnan(LHS) or math.isnan(RHS):
            neg_q = True
        else:
            neg_q = not (LHS <= RHS + 1e-9)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: (\\Omega, \\Sigma, \\mu) is a measure space",
    "H_2: p \\ge 2",
    "H_3: g \\in L^p(\\mu)",
    "\\neg Q: Conclusion fails"
]

N_HYP = 3
NEG_Q_INDEX = 3