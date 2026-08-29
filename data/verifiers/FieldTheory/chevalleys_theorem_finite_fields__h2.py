import sympy
from sympy import Poly, symbols, sympify
from sympy.ntheory import factorint, isprime
import itertools

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false Chevalley's Theorem conjecture.
    Expected witness format: a dictionary {'q': int, 'n': int, 'f': expr/callable/string}
    or a tuple (q, n, f).
    """
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
            f = witness.get('f')
        else:
            q, n, f = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F_q is a finite field (q must be a prime power)
    try:
        if q is None or q < 2:
            h1 = False
        else:
            factors = factorint(q)
            h1 = len(factors) == 1
    except Exception:
        h1 = False

    # H_2: The total degree of f is strictly less than n
    try:
        if n > 0:
            vars = symbols(f'x1:{n+1}')
        else:
            vars = ()
            
        if callable(f):
            if n > 0:
                f_expr = f(*vars)
            else:
                f_expr = f()
        else:
            f_expr = sympify(f)
            
        p = Poly(f_expr, *vars)
        deg = p.total_degree()
        h2 = bool(deg < n)
    except Exception:
        h2 = False

    # H_3: There exists at least one point in F_q^n such that f = 0
    # ¬Q: There is NO other distinct point in F_q^n such that f = 0 (i.e., exactly 1 root)
    try:
        if not h1:
            h3 = False
            neg_q = False
        else:
            if n == 0:
                # F_q^0 has exactly one point: the empty tuple ()
                val = f_expr.subs({})
                if val == 0:
                    roots = 1
                else:
                    roots = 0
            else:
                if isprime(q):
                    roots = 0
                    for pt in itertools.product(range(q), repeat=n):
                        if callable(f):
                            val = f(*pt)
                        else:
                            val = f_expr.subs(dict(zip(vars, pt)))
                        
                        val = sympify(val)
                        if val.is_Integer and val % q == 0:
                            roots += 1
                        elif val == 0:
                            roots += 1
                else:
                    # For non-prime prime powers with n > 0, evaluation requires GF(q) arithmetic.
                    # Since the only valid counterexample is n=0, we can safely return False here
                    # if a user attempts an impossible n > 0 counterexample over a non-prime field.
                    return [h1, h2, False, False]
                    
            h3 = roots >= 1
            neg_q = roots == 1
    except Exception:
        h3 = False
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field",
    "H_2: The total degree of f is strictly less than n",
    "H_3: There exists at least one point in F_q^n such that f = 0",
    "¬Q: There is NO other distinct point in F_q^n such that f = 0"
]

N_HYP = 3
NEG_Q_INDEX = 3