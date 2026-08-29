import sympy
from sympy import symbols, expand
from sympy.ntheory import factorint

x, y = symbols('x y')

def conditions(witness):
    try:
        F, a, P, Q = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: The characteristic of F is not equal to 2
    try:
        if isinstance(F, int):
            char = abs(F)
        elif hasattr(F, 'characteristic'):
            char = F.characteristic()
        elif hasattr(F, 'char'):
            char = F.char
        else:
            char = 0
        h1 = (char != 2)
    except Exception:
        h1 = False
        
    # H2: a in F is a non-zero element
    try:
        if isinstance(F, int) and F > 0:
            h2 = (a % F != 0)
        else:
            h2 = (a != 0)
    except Exception:
        h2 = False
        
    # H3: a is not a perfect square in F
    try:
        if isinstance(F, int) and F > 0:
            h3 = not any((k**2 - a) % F == 0 for k in range(F))
        else:
            from sympy import sqrt
            h3 = not sqrt(a).is_rational
    except Exception:
        h3 = False
        
    # ¬Q: The polynomial x^2 - a y^2 is reducible
    try:
        P_sym = sympy.sympify(P, locals={'x': x, 'y': y})
        Q_sym = sympy.sympify(Q, locals={'x': x, 'y': y})
            
        P_exp = expand(P_sym)
        Q_exp = expand(Q_sym)
        
        def is_unit(poly, n):
            if n == 0:
                return not poly.has(x, y) and poly != 0
            coeffs = poly.as_coefficients_dict()
            const = coeffs.pop(1, 0)
            if sympy.gcd(int(const), n) != 1:
                return False
            rad = 1
            for p in factorint(n):
                rad *= p
            for c in coeffs.values():
                if int(c) % rad != 0:
                    return False
            return True

        n = abs(F) if isinstance(F, int) else 0
        
        if is_unit(P_exp, n) or is_unit(Q_exp, n):
            neg_q = False
        else:
            prod = expand(P_exp * Q_exp)
            target = expand(x**2 - a * y**2)
            diff = expand(prod - target)
            
            if n > 0:
                coeffs = diff.as_coefficients_dict()
                neg_q = all(int(c) % n == 0 for c in coeffs.values())
            else:
                neg_q = (diff == 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: The characteristic of F is not equal to 2",
    "H_2: a in F is a non-zero element",
    "H_3: a is not a perfect square in F",
    "\u00acQ: The polynomial x^2 - a y^2 is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3