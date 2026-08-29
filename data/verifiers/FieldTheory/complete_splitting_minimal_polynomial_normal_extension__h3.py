import sympy
from sympy import factor_list, minpoly, simplify, degree
from sympy.abc import x

def parse_witness(witness):
    """
    Parses the witness into F_gens, E_gens, and alpha.
    Supports formats:
      - (F_gens, E_gens, alpha)
      - (E_gens, alpha)  -> assumes F_gens = []
      - alpha            -> assumes F_gens = [], E_gens = []
    """
    if isinstance(witness, tuple):
        if len(witness) == 3 and isinstance(witness[0], (list, tuple)) and isinstance(witness[1], (list, tuple)):
            return list(witness[0]), list(witness[1]), witness[2]
        elif len(witness) == 2 and isinstance(witness[0], (list, tuple)):
            return [], list(witness[0]), witness[1]
    return [], [], witness

def get_extension_gens(gens, x_var):
    """Filters out rational numbers from generators to avoid SymPy extension errors."""
    ext = []
    for g in gens:
        try:
            if degree(minpoly(g, x_var), x_var) > 1:
                ext.append(g)
        except Exception:
            pass
    return ext

def is_root(f, g, x_var):
    """Checks if g is a root of the polynomial f."""
    try:
        val = f.subs(x_var, g)
        if simplify(val) == 0:
            return True
        if abs(complex(val.evalf(chop=True))) < 1e-9:
            return True
    except Exception:
        pass
    return False

def minpoly_over_F(g, F_gens, x_var):
    """Computes the minimal polynomial of g over the field F = Q(F_gens)."""
    try:
        P = minpoly(g, x_var)
    except Exception:
        raise ValueError("Not algebraic")
    
    ext_gens = get_extension_gens(F_gens, x_var)
    if not ext_gens:
        return P
    try:
        facs = factor_list(P, extension=ext_gens)[1]
        for f, _ in facs:
            if is_root(f, g, x_var):
                return f
    except Exception:
        pass
    return P

def splits_completely(poly, gens, x_var):
    """Checks if the polynomial splits completely into linear factors over Q(gens)."""
    try:
        ext_gens = get_extension_gens(gens, x_var)
        if not ext_gens:
            facs = factor_list(poly)[1]
        else:
            facs = factor_list(poly, extension=ext_gens)[1]
        for f, mult in facs:
            if degree(f, x_var) > 1:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    F_gens, E_gens, alpha = parse_witness(witness)
    
    # H1: E/F is an algebraic field extension
    h1_ok = False
    try:
        h1_ok = True
        for g in F_gens + E_gens:
            minpoly(g, x)
    except Exception:
        h1_ok = False
        
    # H2: The extension E/F is normal
    h2_ok = False
    try:
        all_gens = F_gens + E_gens
        h2_ok = True
        for g in E_gens:
            mf = minpoly_over_F(g, F_gens, x)
            if not splits_completely(mf, all_gens, x):
                h2_ok = False
                break
    except Exception:
        h2_ok = False
        
    # ¬Q: The minimal polynomial of alpha over F does NOT factor completely into linear polynomials in E
    neg_q_ok = False
    try:
        minpoly(alpha, x) # alpha must be algebraic
        all_gens = F_gens + E_gens
        mf_alpha = minpoly_over_F(alpha, F_gens, x)
        neg_q_ok = not splits_completely(mf_alpha, all_gens, x)
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: E over F is an algebraic field extension",
    "H_2: The extension E over F is normal",
    "not Q: The minimal polynomial of alpha over F does NOT factor completely into linear polynomials in E"
]

N_HYP = 2
NEG_Q_INDEX = 2