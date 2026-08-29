import sympy
from sympy import S
import math

Z = S.Integers
Q = S.Rationals

def conditions(witness):
    try:
        if len(witness) == 3:
            R, S_set, s = witness
        elif len(witness) == 2:
            R = Z
            S_set, s = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring with identity
    try:
        h1 = False
        if R in (Z, Q):
            h1 = True
        elif isinstance(R, int) and R > 1:
            h1 = True
    except Exception:
        h1 = False

    # H2: S is a multiplicatively closed subset of R
    try:
        h2 = True
        try:
            S_list = []
            for i, x in enumerate(S_set):
                if i > 100:
                    h2 = False
                    break
                S_list.append(x)
            if len(S_list) == 0:
                h2 = False
        except Exception:
            h2 = False
            S_list = []
            
        if h2:
            for x in S_list:
                if R == Z:
                    sym_x = sympy.sympify(x)
                    if not (isinstance(x, int) or sym_x.is_integer == True):
                        h2 = False
                elif R == Q:
                    sym_x = sympy.sympify(x)
                    if not (sym_x.is_rational == True or sym_x.is_integer == True or isinstance(x, (int, float))):
                        h2 = False
                elif isinstance(R, int) and R > 1:
                    sym_x = sympy.sympify(x)
                    if not (isinstance(x, int) or sym_x.is_integer == True):
                        h2 = False
                    else:
                        if not (0 <= int(x) < R):
                            h2 = False
            
            if h2:
                for a in S_list:
                    for b in S_list:
                        if R in (Z, Q):
                            prod = a * b
                            if not any(prod == c for c in S_list):
                                h2 = False
                                break
                        elif isinstance(R, int) and R > 1:
                            prod = (int(a) * int(b)) % R
                            if not any(prod == int(c) for c in S_list):
                                h2 = False
                                break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H3: 1 is in S
    try:
        h3 = any(x == 1 for x in S_list)
    except Exception:
        h3 = False

    # neg_Q: s/1 is NOT a unit in S^(-1)R
    try:
        if R == Z or (isinstance(R, int) and R > 1):
            sym_s = sympy.sympify(s)
            if not (isinstance(s, int) or sym_s.is_integer == True):
                raise ValueError("s must be an integer")
        elif R == Q:
            sym_s = sympy.sympify(s)
            if not (sym_s.is_rational == True or sym_s.is_integer == True or isinstance(s, (int, float))):
                raise ValueError("s must be a rational")

        is_unit = False
        for v in S_list:
            if R == Z:
                s_val = int(s)
                v_val = int(v)
                if s_val == 0:
                    if v_val == 0: is_unit = True
                else:
                    if v_val % s_val == 0: is_unit = True
            elif R == Q:
                if s == 0:
                    if v == 0: is_unit = True
                else:
                    is_unit = True
            elif isinstance(R, int) and R > 1:
                s_val = int(s)
                v_val = int(v)
                g = math.gcd(s_val, R)
                if v_val % g == 0:
                    is_unit = True
        neg_q = not is_unit
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: 1 is in S",
    "¬Q: The fraction s/1 is not a unit in the ring of fractions S^(-1)R"
]

N_HYP = 3
NEG_Q_INDEX = 3