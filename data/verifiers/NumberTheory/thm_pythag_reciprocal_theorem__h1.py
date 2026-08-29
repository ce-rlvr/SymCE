import sympy

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = sympy.sympify(witness['a'])
            b = sympy.sympify(witness['b'])
            c = sympy.sympify(witness['c'])
            if 'h' in witness:
                h = sympy.sympify(witness['h'])
            else:
                area_sq_16 = 4 * a**2 * b**2 - (a**2 + b**2 - c**2)**2
                h = sympy.sqrt(area_sq_16) / (2 * c)
        else:
            if len(witness) == 4:
                a, b, c, h = [sympy.sympify(x) for x in witness]
            elif len(witness) == 3:
                a, b, c = [sympy.sympify(x) for x in witness]
                area_sq_16 = 4 * a**2 * b**2 - (a**2 + b**2 - c**2)**2
                h = sympy.sqrt(area_sq_16) / (2 * c)
            else:
                return [False, False]
                
        h1_ok = False
        if a > 0 and b > 0 and c > 0 and h > 0:
            if a + b > c and a + c > b and b + c > a:
                area_sq_16 = 4 * a**2 * b**2 - (a**2 + b**2 - c**2)**2
                diff = sympy.simplify(4 * h**2 * c**2 - area_sq_16)
                is_zero = False
                if diff == 0:
                    is_zero = True
                else:
                    try:
                        if abs(float(diff)) < 1e-9:
                            is_zero = True
                    except Exception:
                        pass
                if is_zero:
                    h1_ok = True
    except Exception:
        h1_ok = False

    try:
        if isinstance(witness, dict):
            a = sympy.sympify(witness['a'])
            b = sympy.sympify(witness['b'])
            c = sympy.sympify(witness['c'])
            if 'h' in witness:
                h = sympy.sympify(witness['h'])
            else:
                area_sq_16 = 4 * a**2 * b**2 - (a**2 + b**2 - c**2)**2
                h = sympy.sqrt(area_sq_16) / (2 * c)
        else:
            if len(witness) == 4:
                a, b, c, h = [sympy.sympify(x) for x in witness]
            elif len(witness) == 3:
                a, b, c = [sympy.sympify(x) for x in witness]
                area_sq_16 = 4 * a**2 * b**2 - (a**2 + b**2 - c**2)**2
                h = sympy.sqrt(area_sq_16) / (2 * c)
            else:
                return [h1_ok, False]
                
        left = 1 / a**2 + 1 / b**2
        right = 1 / h**2
        diff = sympy.simplify(left - right)
        is_zero = False
        if diff == 0:
            is_zero = True
        else:
            try:
                if abs(float(diff)) < 1e-9:
                    is_zero = True
            except Exception:
                pass
        neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: h is the altitude to side c in a valid triangle with sides a, b, c",
    "¬Q: 1/a^2 + 1/b^2 != 1/h^2"
]

N_HYP = 1
NEG_Q_INDEX = 1