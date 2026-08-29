import sympy
from sympy import Poly, symbols
from sympy.abc import x, y, z, t, u, v, w

X, Y, Z = symbols('X Y Z')

def conditions(witness) -> list[bool]:
    f, X_var, a = None, None, None

    # Flexible witness unpacking
    if isinstance(witness, dict):
        f = witness.get('f')
        X_var = witness.get('X')
        a = witness.get('a')
        if a is None and f is not None and X_var is not None:
            try:
                a = Poly(f, X_var).LC()
            except Exception:
                pass
    elif isinstance(witness, tuple):
        if len(witness) == 3:
            f, X_var, a = witness
        elif len(witness) == 2:
            f, X_or_a = witness
            if isinstance(X_or_a, sympy.Symbol):
                X_var = X_or_a
                try:
                    a = Poly(f, X_var).LC()
                except Exception:
                    a = None
            else:
                a = X_or_a
                try:
                    free = sorted(list(sympy.sympify(f).free_symbols), key=lambda s: s.name)
                    X_var = free[0] if free else symbols('X')
                except Exception:
                    X_var = symbols('X')
        elif len(witness) == 1:
            f = witness[0]
            try:
                free = sorted(list(sympy.sympify(f).free_symbols), key=lambda s: s.name)
                X_var = free[0] if free else symbols('X')
                a = Poly(f, X_var).LC()
            except Exception:
                X_var = symbols('X')
                a = None
    else:
        f = witness
        try:
            free = sorted(list(sympy.sympify(f).free_symbols), key=lambda s: s.name)
            X_var = free[0] if free else symbols('X')
            a = Poly(f, X_var).LC()
        except Exception:
            X_var = symbols('X')
            a = None

    if f is None or X_var is None or a is None:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        p_f = Poly(f, X_var)
        if p_f.is_zero:
            deg = 0
        else:
            deg = p_f.degree()
        
        # Create a joint polynomial to determine the coefficient ring R
        joint_p = Poly(f + a * X_var**(deg + 1), X_var)
        R = joint_p.domain
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    # H_2: f is a non-zero polynomial over R
    try:
        h2 = not bool(p_f.is_zero)
    except Exception:
        h2 = False

    # neg_Q: The content of f is NOT associate to a in R
    try:
        p_f_joint = Poly(f, X_var, domain=R)
        coeffs = p_f_joint.coeffs()
        
        if not coeffs:
            content = R.zero
        else:
            content = coeffs[0]
            for c in coeffs[1:]:
                content = R.gcd(content, c)
                
        a_sym = sympy.sympify(a)
        a_dom = R.from_sympy(a_sym)
        
        def is_divisible(num, den, dom):
            if den == dom.zero:
                return num == dom.zero
            try:
                dom.exquo(num, den)
                return True
            except Exception:
                return False
                
        # Elements are associate if they divide each other
        assoc = is_divisible(content, a_dom, R) and is_divisible(a_dom, content, R)
        neg_q = not assoc
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a non-zero polynomial over R",
    "¬Q: The content of f is not associate to a in R"
]

N_HYP = 2
NEG_Q_INDEX = 2