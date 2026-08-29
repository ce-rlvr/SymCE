import sympy
from sympy import Poly, Symbol, ZZ, QQ

Z = ZZ
Q = QQ

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f splits completely over R as f(x) = a(x-r_1)...(x-r_n)",
    "¬Q: The content of f is not associate to a in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            f = witness.get('f')
            a = witness.get('a')
            roots = witness.get('roots')
            x = witness.get('x', Symbol('x'))
        else:
            R = witness[0]
            f = witness[1]
            a = witness[2]
            roots = witness[3]
            x = witness[4] if len(witness) > 4 else Symbol('x')
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    try:
        try:
            a_sym = sympy.sympify(a)
            a_R = R.from_sympy(a_sym)
            a_in_R = True
        except Exception:
            a_in_R = False

        try:
            roots_in_R = True
            for r in roots:
                r_sym = sympy.sympify(r)
                R.from_sympy(r_sym)
        except Exception:
            roots_in_R = False

        if not (a_in_R and roots_in_R):
            h2 = False
        else:
            expected_f = a_sym
            for r in roots:
                expected_f = expected_f * (x - sympy.sympify(r))
            
            f_poly = Poly(f, x, domain=R)
            expected_poly = Poly(expected_f, x, domain=R)
            h2 = (f_poly == expected_poly)
    except Exception:
        h2 = False

    try:
        f_poly = Poly(f, x, domain=R)
        
        if f_poly.is_zero:
            is_assoc = False
        else:
            c = f_poly.content()
            
            try:
                a_R = R.from_sympy(sympy.sympify(a))
            except Exception:
                a_R = a
            
            try:
                q1 = R.exquo(c, a_R)
                q2 = R.exquo(a_R, c)
                is_assoc = True
            except Exception:
                is_assoc = False
                
        neg_q = not is_assoc
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]