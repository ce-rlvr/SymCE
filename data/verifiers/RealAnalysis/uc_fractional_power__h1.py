import sympy
import math

# Top-level setup
x = sympy.Symbol('x', real=True, nonnegative=True)

def get_c(witness):
    """
    Extracts the exponent c if the witness is a number c, 
    a callable representing x^c, or a sympy expression representing x^c.
    """
    # 1. Try to interpret witness directly as a number c
    try:
        return float(witness)
    except Exception:
        pass
    
    # 2. Try to interpret witness as a callable f(x) = x^c
    try:
        if callable(witness):
            v2 = float(witness(2))
            v4 = float(witness(4))
            if v2 > 0 and v4 > 0:
                c = math.log(v4 / v2) / math.log(2)
                v3 = float(witness(3))
                if math.isclose(v3, 3**c, rel_tol=1e-4):
                    return c
    except Exception:
        pass

    # 3. Try to interpret witness as a sympy expression x^c
    try:
        if isinstance(witness, sympy.Expr):
            syms = witness.free_symbols
            if len(syms) == 1:
                sym = list(syms)[0]
                v2 = float(witness.subs(sym, 2))
                v4 = float(witness.subs(sym, 4))
                if v2 > 0 and v4 > 0:
                    c = math.log(v4 / v2) / math.log(2)
                    v3 = float(witness.subs(sym, 3))
                    if math.isclose(v3, 3**c, rel_tol=1e-4):
                        return c
            elif len(syms) == 0:
                return float(witness)
    except Exception:
        pass
    
    return None

def conditions(witness) -> list[bool]:
    c = get_c(witness)
    
    # H_1: f: [0, \infty) -> R is defined by f(x) = x^c
    # For x^c to be well-defined and real-valued on [0, \infty), we need c >= 0.
    try:
        h1_ok = (c is not None) and (c >= 0)
    except Exception:
        h1_ok = False
        
    # ¬Q: f is NOT uniformly continuous on [0, \infty)
    # The function x^c is uniformly continuous on [0, \infty) iff c <= 1.
    # Therefore, it fails to be uniformly continuous iff c > 1.
    try:
        neg_q_ok = (c is not None) and (c > 1)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(x) = x^c is defined on [0, infinity)",
    "¬Q: f is not uniformly continuous on [0, infinity)"
]

N_HYP = 1
NEG_Q_INDEX = 1