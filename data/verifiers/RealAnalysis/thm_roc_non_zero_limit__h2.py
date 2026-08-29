import sympy
from sympy import Symbol, limit, oo, Abs

# Top-level setup
n = Symbol('n', integer=True, nonnegative=True)
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    Witness is expected to be a tuple: (a_n, L)
    where a_n is a sympy expression in terms of n (or a callable),
    and L is a real number.
    """
    try:
        a_n_input, L = witness
    except Exception:
        return [False, False, False]
        
    try:
        if callable(a_n_input):
            expr = a_n_input(n)
        else:
            expr = a_n_input
    except Exception:
        return [False, False, False]

    # H_1: (a_n) is a sequence of real numbers
    h1_ok = True
    try:
        for i in range(20):
            val = expr.subs(n, i).evalf()
            # If sympy cannot trivially determine it is real, check numerically
            if not val.is_real:
                cval = complex(val)
                if abs(cval.imag) > 1e-9:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # H_2: L != 0
    try:
        h2_ok = False
        if abs(complex(L)) > 1e-9:
            h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: The radius of convergence of the power series is NOT exactly 1
    neg_q = False
    R_found = False
    R = None
    
    # Attempt 1: Ratio Test
    try:
        ratio = Abs(expr / expr.subs(n, n + 1))
        R_val = limit(ratio, n, oo)
        if not R_val.is_nan and (R_val.is_number or R_val == oo):
            R = R_val
            R_found = True
    except Exception:
        pass

    # Attempt 2: Root Test
    if not R_found:
        try:
            root = Abs(expr)**(1/n)
            L_root = limit(root, n, oo)
            if not L_root.is_nan and (L_root.is_number or L_root == oo):
                if L_root == 0:
                    R = oo
                elif L_root == oo:
                    R = 0
                else:
                    R = 1 / L_root
                R_found = True
        except Exception:
            pass

    if R_found:
        neg_q = bool(R != 1)
    else:
        # Fallback: approximate the radius of convergence for large n
        try:
            val1 = abs(complex(expr.subs(n, 100).evalf()))
            val2 = abs(complex(expr.subs(n, 101).evalf()))
            if val2 != 0:
                approx_R = val1 / val2
                if abs(approx_R - 1.0) > 1e-3:
                    neg_q = True
            else:
                # If terms eventually become 0, the radius is infinity
                neg_q = True
        except Exception:
            pass

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: (a_n) is a sequence of real numbers",
    "H_2: L != 0",
    "¬Q: The radius of convergence of the power series is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2