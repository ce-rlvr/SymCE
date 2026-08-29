import sympy as sp

x = sp.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f, n, x_sym = witness
            elif len(witness) == 2:
                f, n = witness
                x_sym = x
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        f = sp.sympify(f)
        n = sp.sympify(n)
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        p = sp.Poly(f, x_sym)
        H1_ok = bool(p.domain.is_UFD)
    except Exception:
        H1_ok = False

    # H_2: n is the degree of f(x)
    try:
        deg = sp.degree(f, x_sym)
        H2_ok = bool(n == deg)
    except Exception:
        H2_ok = False

    # neg_Q: The content of x^n f(1/x) is NOT equal to the content of f(x) up to a unit
    try:
        p = sp.Poly(f, x_sym)
        c_f = p.content()
        
        try:
            is_neg = bool(n < 0)
        except Exception:
            is_neg = False
            
        if is_neg:
            conclusion_holds = False
        else:
            rev_f = sp.expand(x_sym**n * f.subs(x_sym, 1/x_sym))
            p_rev = sp.Poly(rev_f, x_sym)
            c_rev = p_rev.content()
            
            if c_f == c_rev or c_f == -c_rev:
                conclusion_holds = True
            else:
                if p.domain.is_Field and c_f != 0 and c_rev != 0:
                    conclusion_holds = True
                else:
                    conclusion_holds = False
    except Exception:
        conclusion_holds = False

    try:
        neg_Q_ok = not conclusion_holds
    except Exception:
        neg_Q_ok = False

    return [H1_ok, H2_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: n is the degree of f(x)",
    "¬Q: The content of x^n f(1/x) is NOT equal to the content of f(x) up to a unit"
]

N_HYP = 2
NEG_Q_INDEX = 2