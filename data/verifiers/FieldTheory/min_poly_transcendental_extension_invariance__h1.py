import sympy
from sympy import Symbol, Rational, Poly, primitive, ZZ, QQ
from sympy.abc import x, t

# Top-level setup
# For FieldTheory, we primarily use SymPy's domains (ZZ, QQ) and symbols.

CONDITION_LABELS = [
    "H_1: α is algebraic over F",
    "H_2: t is an element transcendental over F(α)",
    "¬Q: The minimal polynomial of α over the field F(t) is not equal to the minimal polynomial of α over F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample.
    The witness is expected to be a tuple (F, alpha, t) or (alpha, t) with implicit F=ZZ.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                # Try to unpack based on types
                if hasattr(witness[0], 'is_Field') or witness[0] in (ZZ, QQ):
                    F, alpha, t_sym = witness
                elif hasattr(witness[1], 'is_Field') or witness[1] in (ZZ, QQ):
                    alpha, F, t_sym = witness
                else:
                    F, alpha, t_sym = witness
            elif len(witness) == 2:
                alpha, t_sym = witness
                F = ZZ
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: α is algebraic over F
    try:
        # If minpoly succeeds over QQ, alpha is algebraic over QQ (and thus over ZZ)
        mp_QQ = sympy.minpoly(alpha, x)
        h1 = True
    except Exception:
        h1 = False

    # H2: t is an element transcendental over F(α)
    try:
        if isinstance(t_sym, Symbol):
            if hasattr(alpha, 'free_symbols'):
                h2 = t_sym not in alpha.free_symbols
            else:
                h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The minimal polynomial of α over the field F(t) is not equal to the minimal polynomial of α over F
    try:
        # Minimal polynomial over F(t)
        # For F=ZZ or F=QQ, F(t) is QQ(t), and the minimal polynomial is the same as over QQ (monic)
        mp_Ft = sympy.minpoly(alpha, x)
        
        # Minimal polynomial over F
        if F == ZZ:
            # The minimal polynomial over ZZ is the primitive polynomial in ZZ[x]
            poly = Poly(mp_Ft, x)
            lcm = 1
            for c in poly.coeffs():
                if hasattr(c, 'q'):
                    lcm = sympy.lcm(lcm, c.q)
            p_Z = mp_Ft * lcm
            cont, mp_F = primitive(p_Z)
        elif F == QQ:
            mp_F = mp_Ft
        else:
            # Fallback for other domains if supported
            mp_F = sympy.minpoly(alpha, x, domain=F)
            
        # The conclusion fails if the polynomials are not strictly equal
        neg_q = bool(sympy.expand(mp_Ft) != sympy.expand(mp_F))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]