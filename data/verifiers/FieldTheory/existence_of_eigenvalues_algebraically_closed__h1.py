import sympy
from sympy import Matrix

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    # H1: V is a finite-dimensional vector space over K of dimension n >= 1
    try:
        h1 = isinstance(witness, Matrix) and witness.shape[0] >= 1
    except Exception:
        h1 = False

    # H2: T is a linear operator mapping V to V
    try:
        h2 = isinstance(witness, Matrix) and witness.is_square
    except Exception:
        h2 = False

    # neg_Q: There does NOT exist a non-zero vector v in V and a scalar lambda in K such that T(v) = lambda v.
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            is_exact_rational = True
            is_complex = False
            
            for e in witness:
                if hasattr(e, 'is_real') and e.is_real is False:
                    is_complex = True
                    break
                if isinstance(e, float) or (hasattr(e, 'is_Float') and e.is_Float):
                    is_exact_rational = False
                elif hasattr(e, 'is_rational'):
                    if e.is_rational is not True:
                        is_exact_rational = False
                elif not isinstance(e, int):
                    is_exact_rational = False
            
            if is_complex:
                # Over C (or any algebraically closed field), every operator has an eigenvalue.
                has_eval = True
            elif is_exact_rational:
                # Over Q, check for rational roots of the characteristic polynomial.
                rts = sympy.roots(witness.charpoly(), domain='QQ')
                has_eval = len(rts) > 0
            else:
                # Over R, check for real eigenvalues.
                evs = witness.eigenvals()
                has_eval = any((v.is_real is True) for v in evs)
            
            neg_q = not has_eval
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over K of dimension n >= 1",
    "H_2: T is a linear operator mapping V to V",
    "¬Q: T has no eigenvalues in K"
]

N_HYP = 2
NEG_Q_INDEX = 2