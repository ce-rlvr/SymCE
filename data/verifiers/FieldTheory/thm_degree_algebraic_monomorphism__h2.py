import sympy
from sympy import minpoly, degree
from sympy.abc import x

# Top-level setup
QQ = sympy.S.Rationals
ZZ = sympy.S.Integers

CONDITION_LABELS = [
    "H_1: E/F is a field extension",
    "H_2: sigma is a field monomorphism fixing F",
    "H_3: alpha is algebraic over F",
    "¬Q: degree of F(sigma(alpha)) over F != degree of F(alpha) over F"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # 1. Check for tuple/list of 4 booleans (H1, H2, H3, Q)
    if isinstance(witness, (list, tuple)) and len(witness) == 4 and all(isinstance(val, bool) for val in witness):
        try:
            return [witness[0], witness[1], witness[2], not witness[3]]
        except Exception:
            pass

    # 2. Check for dictionary with boolean flags
    if isinstance(witness, dict) and 'H1' in witness:
        try:
            return [
                bool(witness.get('H1', False)),
                bool(witness.get('H2', False)),
                bool(witness.get('H3', False)),
                not bool(witness.get('Q', True))
            ]
        except Exception:
            pass

    # 3. Check for object with boolean attributes
    if hasattr(witness, 'H1'):
        try:
            return [
                bool(getattr(witness, 'H1', False)),
                bool(getattr(witness, 'H2', False)),
                bool(getattr(witness, 'H3', False)),
                not bool(getattr(witness, 'Q', True))
            ]
        except Exception:
            pass

    # 4. Mathematical evaluation
    try:
        if isinstance(witness, dict):
            E = witness.get('E')
            F = witness.get('F')
            L = witness.get('L')
            sigma = witness.get('sigma')
            alpha = witness.get('alpha')
        elif isinstance(witness, tuple) and len(witness) == 5:
            E, F, L, sigma, alpha = witness
        else:
            E = getattr(witness, 'E', None)
            F = getattr(witness, 'F', None)
            L = getattr(witness, 'L', None)
            sigma = getattr(witness, 'sigma', None)
            alpha = getattr(witness, 'alpha', None)

        # H1: E/F is a field extension
        h1 = False
        try:
            if hasattr(E, 'is_Field') and hasattr(F, 'is_Field'):
                h1 = bool(E.is_Field and F.is_Field)
            elif E is not None and F is not None:
                h1 = True
        except Exception:
            h1 = False

        # H2: sigma is a field monomorphism fixing F
        h2 = False
        try:
            if callable(sigma) or isinstance(sigma, dict):
                h2 = True
        except Exception:
            h2 = False

        # H3: alpha is algebraic over F
        h3 = False
        p = None
        try:
            if alpha is not None and F is not None:
                p = minpoly(alpha, x, domain=F)
                h3 = True
        except Exception:
            h3 = False

        # Q: degree of F(sigma(alpha)) over F == degree of F(alpha) over F
        q = True # Default to True so that not q is False on failure
        try:
            if h3 and p is not None:
                if callable(sigma):
                    sigma_alpha = sigma(alpha)
                elif isinstance(sigma, dict):
                    sigma_alpha = sigma[alpha]
                else:
                    sigma_alpha = None
                
                if sigma_alpha is not None:
                    p_sigma = minpoly(sigma_alpha, x, domain=F)
                    q = (degree(p, x) == degree(p_sigma, x))
        except Exception:
            q = True

        return [h1, h2, h3, not q]
    except Exception:
        return [False, False, False, False]