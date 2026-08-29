import sympy

# Top-level setup
oo = sympy.oo

def conditions(witness) -> list[bool]:
    try:
        x, y = witness
    except Exception:
        return [False, False, False]
        
    # H1: x is a real number
    try:
        sx = sympy.sympify(x)
        h1 = bool(sx.is_real == True and len(sx.free_symbols) == 0)
        if not h1:
            if isinstance(x, (int, float)):
                h1 = True
    except Exception:
        h1 = False
        
    # H2: x < y
    try:
        res = x < y
        if res is True:
            h2 = True
        elif res is False:
            h2 = False
        else:
            h2 = bool(res)
    except Exception:
        h2 = False
        
    # neg_Q: There does NOT exist a rational number q such that x < q < y
    neg_q = True
    try:
        # 1. Try simple candidates
        try:
            base_x = sympy.sympify(x)
            if base_x.is_real:
                candidates = [
                    sympy.floor(base_x) + 1,
                    sympy.floor(base_x) + sympy.Rational(1, 2)
                ]
                for q in candidates:
                    if q.is_rational and bool(x < q) and bool(q < y):
                        neg_q = False
                        break
        except Exception:
            pass

        # 2. Try exact rational conversion (handles floats perfectly)
        if neg_q:
            try:
                rx = sympy.Rational(x)
                ry = sympy.Rational(y)
                delta = ry - rx
                if delta > 0:
                    n = sympy.ceiling(1 / delta) + 1
                    m = sympy.floor(n * rx) + 1
                    q = sympy.Rational(m, n)
                    if bool(rx < q) and bool(q < ry):
                        neg_q = False
            except Exception:
                pass
                
        # 3. Fallback for symbolic reals (like pi) or infinity
        if neg_q:
            try:
                if y == sympy.oo:
                    q = sympy.floor(x) + 1
                    if bool(x < q) and bool(q < y):
                        neg_q = False
            except Exception:
                pass
                
        if neg_q:
            try:
                if x == -sympy.oo:
                    q = sympy.ceiling(y) - 1
                    if bool(x < q) and bool(q < y):
                        neg_q = False
            except Exception:
                pass
                
        if neg_q:
            try:
                delta = y - x
                if bool(delta > 0):
                    n = sympy.ceiling(1 / delta) + 1
                    m = sympy.floor(n * x) + 1
                    q = sympy.Rational(m, n)
                    if bool(x < q) and bool(q < y):
                        neg_q = False
            except Exception:
                pass
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is a real number",
    "H_2: x < y",
    "¬Q: There does not exist a rational number q such that x < q < y"
]

N_HYP = 2
NEG_Q_INDEX = 2