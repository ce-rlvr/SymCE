import sympy
from sympy import oo

# Top-level setup: named object bindings that the witness expression may reference.
n = sympy.Symbol('n', integer=True, nonnegative=True)
x = sympy.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (a_expr, x_0)
    where a_expr is a SymPy expression for the n-th coefficient a_n of the power series,
    and x_0 is a real number.
    """
    try:
        a_expr, x_0 = witness
        if callable(a_expr):
            a_expr = a_expr(n)
        a_expr = sympy.sympify(a_expr)
    except Exception:
        return [False, False]

    # H_1: Let \sum_{n=0}^{\infty} a_n x^n be a power series with real coefficients
    try:
        h1_ok = True
        # Check that the first few coefficients evaluate to real numbers
        for i in range(10):
            val = complex(a_expr.subs(n, i).evalf())
            if abs(val.imag) > 1e-9:
                h1_ok = False
                break
        # x_0 must be a valid real number for the context of the conclusion
        x_0_val = float(x_0)
    except Exception:
        h1_ok = False

    # neg_Q: The power series does NOT converge absolutely for all real x such that |x| < |x_0|.
    # This means the radius of convergence R is strictly less than |x_0|.
    try:
        R = None
        if a_expr == 0:
            R = float('inf')
        else:
            # Try the ratio test first: R = lim_{n->oo} |a_n / a_{n+1}|
            try:
                ratio = sympy.Abs(a_expr / a_expr.subs(n, n+1))
                L = sympy.limit(ratio, n, oo)
                if L == oo:
                    R = float('inf')
                elif L.is_number:
                    R = float(L)
            except Exception:
                pass
            
            # Try the root test if the ratio test didn't yield a result: R = 1 / lim_{n->oo} |a_n|^(1/n)
            if R is None:
                try:
                    root = sympy.Abs(a_expr)**(1/n)
                    L = sympy.limit(root, n, oo)
                    if L == 0:
                        R = float('inf')
                    elif L == oo:
                        R = 0.0
                    elif L.is_number:
                        R = 1.0 / float(L)
                except Exception:
                    pass
        
        if R is None:
            neg_q_ok = False
        else:
            neg_q_ok = R < abs(x_0_val)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a_n is a sequence of real coefficients and x_0 is a real number",
    "¬Q: The power series does not converge absolutely for all real x with |x| < |x_0| (i.e., R < |x_0|)"
]

N_HYP = 1
NEG_Q_INDEX = 1