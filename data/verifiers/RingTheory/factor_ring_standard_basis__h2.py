import sympy as sp
from sympy import QQ, ZZ, RR, CC, GF, Poly, Symbol
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a sympy.Poly object or a tuple (Domain, expression).
    """
    try:
        if isinstance(witness, tuple):
            F, p_expr = witness
            if isinstance(p_expr, sp.Poly):
                p = p_expr.set_domain(F)
            else:
                p = sp.Poly(p_expr, domain=F)
        else:
            if isinstance(witness, sp.Poly):
                p = witness
            else:
                p = sp.Poly(witness)
            F = p.domain
    except Exception:
        return [False, False, False]

    # H1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    # H2: The degree of p(x) is n > 0
    try:
        n = p.degree()
        h2 = bool(n > 0)
    except Exception:
        h2 = False

    # neg_Q: The elements 1, x, ..., x^{n-1} do NOT form a basis for the quotient ring
    # In any commutative ring F, 1, ..., x^{n-1} form a basis for F[x]/(p(x)) 
    # if and only if the leading coefficient of p(x) is a unit in F.
    try:
        if n <= 0:
            neg_q = True
        else:
            LC = p.LC()
            is_basis = F.is_unit(LC)
            neg_q = not is_basis
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The degree of p(x) is n > 0",
    "neg_Q: The elements 1, x, ..., x^(n-1) do not form a basis for the quotient ring"
]

N_HYP = 2
NEG_Q_INDEX = 2