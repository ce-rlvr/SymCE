import sympy
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F",
    "H_3: For every element a in F, f(a) = 0",
    "¬Q: f is not the zero polynomial over F"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F_rep = witness.get('p', witness.get('F'))
            expr = witness.get('f', witness.get('expr'))
        elif hasattr(witness, '__iter__') and not isinstance(witness, str):
            witness_list = list(witness)
            F_rep = witness_list[0]
            expr = witness_list[1]
        else:
            F_rep = witness.p
            expr = witness.f
            
        if hasattr(F_rep, 'char'):
            p = int(F_rep.char)
        elif hasattr(F_rep, 'characteristic'):
            p = int(F_rep.characteristic())
        elif isinstance(F_rep, str) and F_rep.startswith('GF('):
            p = int(F_rep[3:-1])
        else:
            p = int(F_rep)
    except Exception:
        p = None
        expr = None

    # H_1: F is a field
    try:
        h1 = p is not None and sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: f is a polynomial over F
    try:
        if not h1 or expr is None:
            h2 = False
        else:
            expr_sym = sympy.sympify(expr)
            free_syms = expr_sym.free_symbols
            if len(free_syms) > 1:
                h2 = False
            else:
                var = list(free_syms)[0] if free_syms else x
                poly_f = sympy.Poly(expr_sym, var, domain=sympy.GF(p))
                h2 = True
    except Exception:
        h2 = False

    # H_3: For every element a in F, f(a) = 0
    try:
        if not h2:
            h3 = False
        else:
            h3 = True
            zero = poly_f.domain.zero
            for a in range(p):
                if poly_f.eval(a) != zero:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # neg_Q: f is not the zero polynomial over F
    try:
        if not h2:
            neg_q = False
        else:
            neg_q = not poly_f.is_zero
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]