import sympy
from sympy import QQ, Symbol, Poly
from sympy.polys.numberfields import primitive_element
from sympy import minpoly

x = Symbol('x')

CONDITION_LABELS = [
    "H_1: F is the field of rational numbers Q",
    "H_2: f(x) = x^4 - 2",
    "¬Q: The degree of the extension E over Q is not 8"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture.
    The witness can be the extension field E, its degree, its primitive element, 
    its minimal polynomial, or a tuple/dict specifying F, f, and E.
    """
    F_val = QQ
    f_val = x**4 - 2
    E_val = witness
    
    if isinstance(witness, tuple):
        if len(witness) == 3:
            F_val, f_val, E_val = witness
        elif len(witness) == 2:
            f_val, E_val = witness
    elif isinstance(witness, dict):
        if 'F' in witness: F_val = witness['F']
        if 'f' in witness: f_val = witness['f']
        if 'E' in witness: E_val = witness['E']

    # H_1: F is the field of rational numbers Q
    try:
        h1_ok = (F_val == QQ) or (str(F_val) in ['QQ', 'Q', 'RationalField', 'Rationals'])
    except Exception:
        h1_ok = False

    # H_2: f(x) = x^4 - 2
    try:
        if isinstance(f_val, Poly):
            expr = f_val.as_expr()
        else:
            expr = f_val
        h2_ok = bool((expr - (x**4 - 2)).simplify() == 0)
    except Exception:
        h2_ok = False

    # ¬Q: The degree of the extension E over Q is not 8
    try:
        deg = None
        if E_val == QQ or str(E_val) in ['QQ', 'Q', 'RationalField', 'Rationals']:
            deg = 1
        elif isinstance(E_val, int):
            deg = E_val
        elif hasattr(E_val, 'is_Integer') and E_val.is_Integer:
            deg = int(E_val)
        elif hasattr(E_val, 'degree'):
            if callable(E_val.degree):
                deg = int(E_val.degree())
            else:
                deg = int(E_val.degree)
        elif hasattr(E_val, 'mod') and hasattr(E_val.mod, 'degree'):
            if callable(E_val.mod.degree):
                deg = int(E_val.mod.degree())
            else:
                deg = int(E_val.mod.degree)
        elif isinstance(E_val, (list, tuple)):
            mp, _ = primitive_element(E_val, x)
            deg = int(mp.degree())
        elif hasattr(E_val, 'free_symbols') and len(E_val.free_symbols) == 1:
            sym = list(E_val.free_symbols)[0]
            if E_val.is_polynomial(sym):
                deg = int(Poly(E_val, sym).degree())
            else:
                mp = minpoly(E_val, x)
                deg = int(mp.degree())
        else:
            mp = minpoly(E_val, x)
            deg = int(mp.degree())
            
        neg_q_ok = bool(deg != 8)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]