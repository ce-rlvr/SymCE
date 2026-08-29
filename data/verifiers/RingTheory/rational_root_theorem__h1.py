import sympy
from sympy import Poly
from sympy.abc import x
import math

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion
    of the modified Rational Root Theorem.
    
    Witness is expected to be a tuple: (f, p, q)
    where f is a sympy expression in x, and p, q are integers.
    """
    try:
        f, p, q = witness
    except Exception:
        return [False, False, False]
        
    # H_1: a_n != 0 and a_0 != 0
    try:
        poly = Poly(f, x)
        a_n = poly.LC()
        a_0 = poly.nth(0)
        h1 = (a_n != 0) and (a_0 != 0)
    except Exception:
        h1 = False

    # H_2: p/q is a rational root of f(x) such that p and q are coprime integers
    try:
        p_int = int(p)
        q_int = int(q)
        if q_int == 0:
            h2 = False
        else:
            coprime = math.gcd(p_int, q_int) == 1
            root_val = sympy.Rational(p_int, q_int)
            is_root = sympy.simplify(f.subs(x, root_val)) == 0
            h2 = coprime and is_root
    except Exception:
        h2 = False

    # ¬Q: p does not divide a_0 or q does not divide a_n
    try:
        def divides(a, b):
            if a == 0:
                return b == 0
            try:
                ratio = sympy.Rational(sympy.simplify(b / a))
                return ratio.q == 1
            except Exception:
                ratio = sympy.simplify(b / a)
                return ratio.is_integer == True

        p_divides_a0 = divides(p_int, a_0)
        q_divides_an = divides(q_int, a_n)
        
        neg_q = not (p_divides_a0 and q_divides_an)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a_n != 0 and a_0 != 0",
    "H_2: p/q is a rational root of f(x) such that p and q are coprime integers",
    "¬Q: p does not divide a_0 or q does not divide a_n"
]

N_HYP = 2
NEG_Q_INDEX = 2