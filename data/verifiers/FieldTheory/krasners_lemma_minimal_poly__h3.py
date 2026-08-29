import sympy
from sympy.abc import x, y, z, t, alpha, beta
from sympy import QQ, ZZ, RR, CC
import math
import itertools
import functools
import z3

# Top-level setup for FieldTheory
# (No specific named bindings required other than standard symbols and domains)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    Since SymPy lacks native support for complete non-archimedean fields (e.g., p-adics)
    and p-adic distances between algebraic numbers, the witness is expected to be a 
    mock object, dictionary, or tuple providing the truth values directly.
    """
    def get_bool(names):
        for name in names:
            if hasattr(witness, name):
                try:
                    val = getattr(witness, name)
                    return bool(val() if callable(val) else val)
                except Exception:
                    pass
            if isinstance(witness, dict) and name in witness:
                try:
                    return bool(witness[name])
                except Exception:
                    pass
        return False

    try:
        if isinstance(witness, (list, tuple)) and len(witness) >= 5:
            if all(isinstance(val, bool) for val in witness[:5]):
                return [
                    bool(witness[0]), 
                    bool(witness[1]), 
                    bool(witness[2]), 
                    bool(witness[3]), 
                    not bool(witness[4])
                ]
    except Exception:
        pass

    try:
        h1 = get_bool(['h1', 'H1', 'is_complete', 'K_is_complete', 'is_complete_non_archimedean'])
    except Exception:
        h1 = False

    try:
        h2 = get_bool(['h2', 'H2', 'is_separable', 'alpha_separable', 'are_separable'])
    except Exception:
        h2 = False

    try:
        h3 = get_bool(['h3', 'H3', 'r_is_min_distance', 'r_correct', 'is_r_min_distance'])
    except Exception:
        h3 = False

    try:
        h4 = get_bool(['h4', 'H4', 'dist_less_than_r', 'distance_less', 'is_dist_less'])
    except Exception:
        h4 = False

    try:
        q = get_bool(['q', 'Q', 'conclusion', 'alpha_in_K_beta', 'is_min_poly_x_minus_alpha'])
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field complete with respect to a non-archimedean absolute value",
    "H_2: α and β are separable algebraic elements over K in a fixed algebraic closure",
    "H_3: r is the minimum distance between α and any of its distinct Galois conjugates",
    "H_4: the distance between α and β is strictly less than r",
    "¬Q: The minimal polynomial of α over K(β) is not exactly x - α (α is not in K(β))"
]

N_HYP = 4
NEG_Q_INDEX = 4