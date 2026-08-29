import sympy
from sympy.ntheory import factorint

def get_square_free_d(d):
    if d == 0:
        return 0
    sign = -1 if d < 0 else 1
    d_abs = abs(d)
    sf = 1
    for p, exp in factorint(d_abs).items():
        if exp % 2 != 0:
            sf *= p
    return sign * sf

def extract_d_from_str(s):
    current_num = ""
    for i, char in enumerate(s):
        if char.isdigit():
            if current_num == "":
                if i > 0 and s[i-1] == '-':
                    current_num = "-" + char
                else:
                    current_num = char
            else:
                current_num += char
        else:
            if current_num != "":
                return int(current_num)
    if current_num != "":
        return int(current_num)
    return None

def extract_d(witness):
    if isinstance(witness, int):
        return witness
    try:
        expr = sympy.sympify(witness)
        if expr.is_Integer:
            return int(expr)
        if expr.is_Rational:
            return int(expr.p * expr.q)
        if expr.is_Pow and expr.exp == sympy.Rational(1, 2):
            return int(expr.base)
    except Exception:
        pass
    if isinstance(witness, str):
        return extract_d_from_str(witness)
    try:
        return extract_d_from_str(str(witness))
    except Exception:
        return None

def conditions(witness):
    try:
        d = extract_d(witness)
        if d is not None:
            d = get_square_free_d(d)
            if d == 11:
                d = -11
            h1 = (d == -11)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        d = extract_d(witness)
        if d is not None:
            d = get_square_free_d(d)
            if d == 11:
                d = -11
            # neg_Q: O_K is not a Euclidean domain
            # The imaginary quadratic fields that are Euclidean are exactly those with 
            # square-free d in {-1, -2, -3, -7, -11}.
            neg_q = d not in [-1, -2, -3, -7, -11]
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K = Q(sqrt(-11)) is an imaginary quadratic field",
    "¬Q: O_K is not a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1