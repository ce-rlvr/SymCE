import sympy
from sympy.abc import x, t

# Top-level setup
# The witness is expected to be a tuple (f, p) where:
#   - f is a SymPy expression in x and t representing the minimal polynomial of the extension over F_p(t)
#   - p is a prime integer representing the characteristic of the field
# Example counterexample: witness = (x**2 - t, 2)

def conditions(witness) -> list[bool]:
    try:
        f, p = witness
    except Exception:
        return [False, False]

    # H_1: Let E/F be an algebraic purely inseparable field extension
    try:
        h1_ok = False
        if sympy.isprime(p):
            f_expr = sympy.sympify(f)
            if f_expr.has(x) and f_expr.has(t):
                deg = sympy.degree(f_expr, x)
                if deg >= 1:
                    temp = deg
                    while temp % p == 0 and temp > 1:
                        temp //= p
                    if temp == 1:
                        remainder = sympy.simplify(f_expr - x**deg)
                        if remainder == -t:
                            h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: The field E is not equal to F
    try:
        neg_q_ok = False
        if h1_ok:
            deg = sympy.degree(sympy.sympify(f), x)
            if deg > 1:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: E/F is an algebraic purely inseparable field extension",
    "¬Q: The field E is not equal to F"
]

N_HYP = 1
NEG_Q_INDEX = 1