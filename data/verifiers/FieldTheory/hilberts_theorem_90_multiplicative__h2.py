import sympy
from sympy import sympify

def conditions(witness):
    """
    witness should be a tuple (d, a, b, sigma_id) or a dict with these keys.
    - d: rational number, not a perfect square, defining L = Q(sqrt(d))
    - a, b: rational numbers defining alpha = a + b*sqrt(d) in L
    - sigma_id: 0 for identity, 1 for conjugation in Gal(L/Q)
    """
    try:
        if isinstance(witness, dict):
            d = witness.get('d')
            a = witness.get('a')
            b = witness.get('b')
            sigma_id = witness.get('sigma_id')
        else:
            d, a, b, sigma_id = witness
    except Exception:
        return [False, False, False]

    try:
        d_sym = sympify(d)
        sigma_id = int(sigma_id)
        is_ext = (d_sym.is_rational is True) and (sympy.sqrt(d_sym).is_rational is not True)
        h1 = bool(is_ext and sigma_id in (0, 1))
    except Exception:
        h1 = False

    try:
        a_sym = sympify(a)
        b_sym = sympify(b)
        h2 = bool((a_sym.is_rational is True) and (b_sym.is_rational is True))
    except Exception:
        h2 = False

    try:
        norm_alpha = a_sym**2 - d_sym * b_sym**2
        P = (norm_alpha == 1)
        
        if sigma_id == 0:
            Q = (a_sym == 1 and b_sym == 0)
        elif sigma_id == 1:
            Q = (norm_alpha == 1)
        else:
            Q = False
            
        neg_q = bool(P != Q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite cyclic Galois extension",
    "H_2: alpha is an element of L",
    "¬Q: N_{L/K}(alpha) = 1 does not imply alpha = beta / sigma(beta) (or vice versa)"
]

N_HYP = 2
NEG_Q_INDEX = 2