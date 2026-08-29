import sympy
from sympy import Poly, QQ, ZZ
from sympy.abc import x

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness can be a dictionary, a tuple (F, f, k), (f, k), or just f.
    """
    F = None
    f_val = None
    k = None

    try:
        if isinstance(witness, dict):
            F = witness.get('F', None)
            f_val = witness.get('f', witness.get('f(x)', None))
            k = witness.get('k', None)
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                F, f_val, k = witness
            elif len(witness) == 2:
                if isinstance(witness[1], (int, sympy.Integer)):
                    f_val, k = witness
                else:
                    F, f_val = witness
            elif len(witness) == 1:
                f_val = witness[0]
        else:
            f_val = witness
    except Exception:
        pass

    if F is None:
        try:
            if hasattr(f_val, 'domain'):
                F = f_val.domain
            else:
                F = QQ
        except Exception:
            F = QQ

    h1 = False
    try:
        if hasattr(F, 'is_Field'):
            h1 = bool(F.is_Field)
        elif F in [sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
            h1 = True
    except Exception:
        h1 = False

    h2 = False
    f_poly = None
    try:
        if isinstance(f_val, Poly):
            f_poly = f_val
        else:
            try:
                f_poly = Poly(f_val, x, domain=F)
            except Exception:
                f_poly = Poly(f_val, x)
        
        if f_poly.is_univariate and f_poly.degree() > 0:
            h2 = True
    except Exception:
        h2 = False

    if k is None and f_poly is not None:
        try:
            k = f_poly.degree()
        except Exception:
            pass

    neg_q = False
    try:
        if h1 and h2 and k is not None:
            factors = f_poly.factor_list()
            m = len(factors[1])
            num_idempotents = 2 ** m
            if num_idempotents != (2 ** int(k)):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a non-constant polynomial over F",
    "¬Q: The factor ring does not contain exactly 2^k idempotent elements"
]

N_HYP = 2
NEG_Q_INDEX = 2