import sympy
from sympy import Symbol, Poly

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Given a witness (expected to be an integer n, or a tuple/dict containing n),
    evaluates the remaining hypotheses and the negated conclusion.
    """
    n = None
    if isinstance(witness, dict) and 'n' in witness:
        n = witness['n']
    elif isinstance(witness, (tuple, list)) and len(witness) > 0:
        n = witness[0]
    else:
        n = witness

    # H_1: Phi_n(x) is the n-th cyclotomic polynomial in Z[x]
    try:
        if isinstance(n, bool):
            h1 = False
        else:
            n_float = float(n)
            n_int = int(n_float)
            if n_float != n_int:
                h1 = False
            else:
                n = n_int
                h1 = (n >= 0)
    except Exception:
        h1 = False

    # not Q: Phi_n(x) is not irreducible over Q
    try:
        if n == 0:
            # The 0-th cyclotomic polynomial is defined as 1 in formal libraries
            poly = sympy.Integer(1)
        elif n > 0:
            poly = sympy.cyclotomic_poly(n, x)
        else:
            poly = None

        if poly is not None:
            if poly == 1 or poly == -1:
                # Units are not irreducible
                neg_q = True
            else:
                p = Poly(poly, x, domain='QQ')
                neg_q = not p.is_irreducible
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Phi_n is the n-th cyclotomic polynomial",
    "not Q: Phi_n is not irreducible over Q"
]

N_HYP = 1
NEG_Q_INDEX = 1