import sympy
from sympy import Poly
from sympy.abc import x
import math

# Top-level setup
# The witness may use x to define polynomial expressions.

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      1. f(x) in F_q[x] is an irreducible polynomial over F_q
      2. The degree of f(x) is n >= 1
      3. m >= 1 is an integer such that gcd(n, m) = 1
    Conclusion:
      f(x) is irreducible over the extension field F_{q^m}
    """
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            m = witness.get('m')
            f_expr = witness.get('f')
        else:
            q, m, f_expr = witness
    except Exception:
        return [False, False, False, False]

    # H1: f(x) in F_q[x] is an irreducible polynomial over F_q
    try:
        q_int = int(q)
        if isinstance(f_expr, Poly):
            f_expr = f_expr.as_expr()
        f = Poly(f_expr, x, modulus=q_int)
        h1 = f.is_irreducible
    except Exception:
        h1 = False

    # H2: The degree of f(x) is n >= 1
    try:
        q_int = int(q)
        if isinstance(f_expr, Poly):
            f_expr = f_expr.as_expr()
        f = Poly(f_expr, x, modulus=q_int)
        n = f.degree()
        h2 = (n >= 1)
    except Exception:
        h2 = False

    # H3: m >= 1 is an integer such that gcd(n, m) == 1
    try:
        q_int = int(q)
        if isinstance(f_expr, Poly):
            f_expr = f_expr.as_expr()
        f = Poly(f_expr, x, modulus=q_int)
        n = f.degree()
        h3 = (m >= 1 and int(m) == m and math.gcd(int(n), int(m)) == 1)
    except Exception:
        h3 = False

    # Negated Conclusion: f(x) is NOT irreducible over F_{q^m}
    try:
        q_int = int(q)
        m_int = int(m)
        if isinstance(f_expr, Poly):
            f_expr = f_expr.as_expr()
        f = Poly(f_expr, x, modulus=q_int)
        n = f.degree()
        
        if n < 1:
            is_irred_Fqm = False
        else:
            is_irred_Fqm = True
            x_poly = Poly(x, x, modulus=q_int)
            # f(x) is irreducible over F_{q^m} iff it has no factors of degree <= n/2 over F_{q^m}.
            # This is equivalent to gcd(f(x), x^{q^{m*k}} - x) == 1 for all 1 <= k <= n/2.
            for k in range(1, n // 2 + 1):
                power = q_int**(m_int * k)
                res = Poly(1, x, modulus=q_int)
                base = x_poly % f
                exp = power
                
                # Modular exponentiation: base^exp mod f
                while exp > 0:
                    if exp % 2 == 1:
                        res = (res * base) % f
                    base = (base * base) % f
                    exp //= 2
                
                rem = (res - x_poly) % f
                g = f.gcd(rem)
                if g.degree() > 0:
                    is_irred_Fqm = False
                    break
                    
        neg_q = not is_irred_Fqm
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is an irreducible polynomial over F_q",
    "H_2: The degree of f(x) is n >= 1",
    "H_3: m >= 1 is an integer such that gcd(n, m) = 1",
    "not Q: f(x) is not irreducible over the extension field F_q^m"
]

N_HYP = 3
NEG_Q_INDEX = 3