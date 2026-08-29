import sympy
from sympy.abc import x
from sympy import Rational, Integer, Poly, degree, isprime, Abs, simplify

# Top-level setup for witness expressions
# (No specific group theory objects needed for this ring theory theorem)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (f, p, c_list)
      - f: a sympy polynomial in x
      - p: a prime number
      - c_list: a list of n distinct integers
    """
    try:
        f, p, c_list = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: The degree n of f(x) satisfies n >= 5
    try:
        n = int(degree(f, x))
        h1 = (n >= 5)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: There exist n distinct integers c_i such that |f(c_i)| = p for all 1 <= i <= n
    try:
        try:
            n_val = int(degree(f, x))
        except Exception:
            n_val = -1
            
        if n_val >= 0 and len(c_list) == n_val and len(set(c_list)) == n_val:
            h3 = True
            for c in c_list:
                # Check if c is an integer
                if int(c) != c:
                    h3 = False
                    break
                # Check if |f(c)| == p
                val = f.subs(x, c)
                if simplify(Abs(val) - p) != 0:
                    h3 = False
                    break
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: f(x) is reducible over Q
    try:
        poly = Poly(f, x, domain='QQ')
        is_irr = poly.is_irreducible
        neg_q = not bool(is_irr)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: The degree n of f(x) satisfies n >= 5",
    "H_2: p is a prime number",
    "H_3: There exist n distinct integers c_i such that |f(c_i)| = p for all 1 <= i <= n",
    "¬Q: f(x) is reducible over Q"
]

N_HYP = 3
NEG_Q_INDEX = 3