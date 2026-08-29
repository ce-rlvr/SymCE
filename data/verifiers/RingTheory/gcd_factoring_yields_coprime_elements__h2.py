import math
import sympy
from sympy import sympify
from sympy.abc import x, y, z, t, u, v, w

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: d is a greatest common divisor of a and b",
    "¬Q: The greatest common divisor of a/d and b/d is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            d = witness.get('d')
            x_val = witness.get('x')
            y_val = witness.get('y')
        else:
            a = witness[0]
            b = witness[1]
            d = witness[2]
            x_val = witness[3] if len(witness) > 3 else None
            y_val = witness[4] if len(witness) > 4 else None
            
        if a is None or b is None or d is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a UFD
    try:
        elements = [a, b, d]
        if x_val is not None: elements.append(x_val)
        if y_val is not None: elements.append(y_val)
        
        has_symbols = False
        for e in elements:
            try:
                if sympify(e).free_symbols:
                    has_symbols = True
                    break
            except Exception:
                pass

        if not has_symbols:
            h1 = True
            for e in elements:
                try:
                    if float(e) != int(e):
                        h1 = False
                        break
                except Exception:
                    h1 = False
                    break
            
            if h1:
                a = int(a)
                b = int(b)
                d = int(d)
                if x_val is not None: x_val = int(x_val)
                if y_val is not None: y_val = int(y_val)
                is_sym = False
        else:
            a = sympify(a)
            b = sympify(b)
            d = sympify(d)
            if x_val is not None: x_val = sympify(x_val)
            if y_val is not None: y_val = sympify(y_val)
            h1 = True
            is_sym = True
    except Exception:
        h1 = False
        is_sym = False

    # H2: d is a greatest common divisor of a and b
    try:
        if not h1:
            h2 = False
        else:
            if is_sym:
                g = sympy.gcd(a, b)
                if d == 0:
                    h2 = (g == 0)
                else:
                    q1, r1 = sympy.div(g, d)
                    q2, r2 = sympy.div(d, g)
                    h2 = (r1 == 0 and r2 == 0)
            else:
                h2 = (abs(d) == math.gcd(a, b))
    except Exception:
        h2 = False

    # Neg_Q: gcd(a/d, b/d) is not a unit
    try:
        if not h1:
            neg_q = False
        else:
            if x_val is not None and y_val is not None:
                if d * x_val == a and d * y_val == b:
                    if is_sym:
                        g = sympy.gcd(x_val, y_val)
                        neg_q = not (g.is_constant() and g != 0)
                    else:
                        neg_q = (math.gcd(x_val, y_val) != 1)
                else:
                    neg_q = False
            else:
                if d == 0:
                    # If d=0, a/d and b/d are undefined or multi-valued.
                    # We can always find valid quotients x, y (e.g., x=2, y=2) 
                    # whose gcd is not a unit, thus the conclusion fails.
                    neg_q = True
                else:
                    if is_sym:
                        x_impl = sympy.simplify(a / d)
                        y_impl = sympy.simplify(b / d)
                        g = sympy.gcd(x_impl, y_impl)
                        neg_q = not (g.is_constant() and g != 0)
                    else:
                        if a % d == 0 and b % d == 0:
                            x_impl = a // d
                            y_impl = b // d
                            neg_q = (math.gcd(x_impl, y_impl) != 1)
                        else:
                            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]