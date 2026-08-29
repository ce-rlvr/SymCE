import sympy
from sympy import Symbol, Poly, simplify, MatrixBase, I, sqrt, Rational
from sympy.polys.domains import QQ, ZZ, RR, CC, GF

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (F, f, a, sym) or (F, f, a).
    """
    try:
        if len(witness) == 4:
            F, f, a, sym = witness
        elif len(witness) == 3:
            F, f, a = witness
            if isinstance(f, Poly):
                free = f.free_symbols
            else:
                free = f.free_symbols if hasattr(f, 'free_symbols') else set()
            sym = list(free)[0] if len(free) == 1 else Symbol('x')
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    # H2: f(x) is a polynomial over F
    try:
        p_f_F = Poly(f, sym, domain=F)
        h2 = True
    except Exception:
        h2 = False

    # neg_Q: (x - a) divides f(x) over F iff f(a) == 0 is FALSE
    try:
        # Check if a is in F
        a_in_F = False
        try:
            if a in F:
                a_in_F = True
        except Exception:
            pass
        if not a_in_F:
            try:
                F.from_sympy(a)
                a_in_F = True
            except Exception:
                a_in_F = False

        # Evaluate P: (x - a) divides f(x) over F
        if a_in_F:
            p_div = Poly(sym - a, sym, domain=F)
            p_f_F = Poly(f, sym, domain=F)
            _, r = p_f_F.div(p_div)
            P_val = r.is_zero
        else:
            P_val = False

        # Evaluate Q: f(a) == 0
        p_f_any = Poly(f, sym)
        if getattr(a, 'is_Matrix', False):
            val = a.zeros(*a.shape)
            degree = p_f_any.degree()
            for i, coeff in enumerate(p_f_any.all_coeffs()):
                power = degree - i
                if power == 0:
                    val += coeff * sympy.eye(a.shape[0])
                else:
                    val += coeff * (a ** power)
            Q_val = val.is_zero_matrix
        else:
            val = p_f_any.eval(a)
            Q_val = (simplify(val) == 0) or (getattr(val, 'expand', lambda: val)() == 0)
            if not Q_val and hasattr(val, 'is_zero'):
                Q_val = (val.is_zero is True)

        # The conclusion is P <==> Q. Its negation is P != Q.
        neg_q = (P_val != Q_val)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F",
    "not Q: x minus a divides f is not equivalent to f evaluated at a is 0"
]

N_HYP = 2
NEG_Q_INDEX = 2