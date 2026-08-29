import sympy
from sympy.polys import cyclotomic_poly
from sympy.abc import x

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (n, p) or a dictionary with keys 'n' and 'p'.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
        else:
            n, p = witness
    except Exception:
        return [False, False, False]
        
    # H1: n >= 1 is an integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n >= 1
    except Exception:
        h1 = False
        
    # H2: p divides n
    try:
        h2 = isinstance(p, (int, sympy.Integer)) and p != 0 and n % p == 0
    except Exception:
        h2 = False
        
    # neg_Q: Phi_{pn}(x) != Phi_n(x^p)
    try:
        if h1 and h2:
            pn = int(p * n)
            # If pn < 1, the standard cyclotomic polynomial Phi_{pn}(x) is undefined,
            # and Phi_n(x^p) involves negative or zero exponents (rational function).
            # Thus, the equality of polynomials fails.
            if pn < 1:
                neg_q = True
            else:
                phi_pn = cyclotomic_poly(pn, x)
                phi_n = cyclotomic_poly(int(n), x)
                phi_n_xp = phi_n.subs(x, x**int(p))
                diff = sympy.expand(phi_pn - phi_n_xp)
                neg_q = diff != 0
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: p divides n",
    "¬Q: Phi_{pn}(x) != Phi_n(x^p)"
]

N_HYP = 2
NEG_Q_INDEX = 2