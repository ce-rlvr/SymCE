import sympy
from sympy import Poly, groebner
from sympy.abc import x, y, z, t, u, v, w

def conditions(witness):
    try:
        # H_1: R is a commutative ring
        # In our sympy setup, the coefficients are from a commutative ring (like ZZ or QQ).
        h1 = True
    except Exception:
        h1 = False

    try:
        # H_2: n is a positive integer
        vars_set = set()
        if isinstance(witness, (list, tuple)):
            for g in witness:
                if isinstance(g, sympy.Expr):
                    vars_set.update(g.free_symbols)
        h2 = len(vars_set) >= 1
    except Exception:
        h2 = False

    try:
        # H_3: I is an ideal of the polynomial ring
        # We verify this by checking if the witness is a non-empty collection of sympy expressions.
        h3 = isinstance(witness, (list, tuple)) and len(witness) > 0 and all(isinstance(g, sympy.Expr) for g in witness)
    except Exception:
        h3 = False

    try:
        # ¬Q: The factor ring does NOT naturally inherit the structure of a graded R-algebra.
        # This happens if and only if the ideal I is NOT a homogeneous ideal.
        # An ideal is homogeneous iff its reduced Groebner basis consists entirely of homogeneous polynomials.
        if not (h2 and h3):
            neg_q = False
        else:
            vars_list = sorted(list(vars_set), key=lambda var: var.name)
            gb = groebner(witness, *vars_list)
            is_hom = True
            for p in gb:
                poly = Poly(p, *vars_list)
                if not poly.is_homogeneous:
                    is_hom = False
                    break
            neg_q = not is_hom
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: n is a positive integer",
    "H_3: I is an ideal of the polynomial ring",
    "¬Q: The ideal I is not homogeneous"
]

N_HYP = 3
NEG_Q_INDEX = 3