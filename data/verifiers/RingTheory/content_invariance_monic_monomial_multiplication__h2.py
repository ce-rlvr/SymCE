import sympy as sp

# Top-level setup for standard algebra objects
# For Ring Theory, we can define some symbols if needed, but integers are used directly.
x, y, z = sp.symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (x_val, k, f_val) representing elements in the UFD Z,
    checks if it is a valid counterexample to the false conjecture.
    
    The dropped hypothesis was that f(x) is a polynomial in R[x] and x is an indeterminate. 
    Without it, f(x) and x can just be elements of R, where the "content" of an element 
    is the element itself (up to associates).
    """
    try:
        x_val, k, f_val = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    # We use the ring of integers Z, which is a UFD.
    try:
        h1_ok = isinstance(x_val, int) and isinstance(f_val, int)
    except Exception:
        h1_ok = False

    # H_2: k >= 1 is an integer
    try:
        h2_ok = isinstance(k, int) and k >= 1
    except Exception:
        h2_ok = False

    # ¬Q: The content of x^k f(x) is NOT associate to the content of f(x) in R
    # In Z, two elements are associate if their absolute values are equal.
    try:
        content_f = abs(f_val)
        content_xk_f = abs((x_val ** k) * f_val)
        neg_q_ok = content_xk_f != content_f
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: k >= 1 is an integer",
    "¬Q: The content of x^k f(x) is not associate to the content of f(x) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2