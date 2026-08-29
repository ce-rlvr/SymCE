import sympy
import math
import itertools
import functools

# Top-level setup
# No named bindings needed for Number Theory

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
            m = witness.get('m')
        else:
            a, b, c, m = witness
    except Exception:
        return [False, False]

    def is_int_like(x):
        if isinstance(x, int): return True
        if hasattr(x, 'is_integer') and x.is_integer: return True
        if isinstance(x, float) and x.is_integer(): return True
        if isinstance(x, sympy.Integer): return True
        return False

    # H1: a, b, and c are integers
    try:
        h1 = is_int_like(a) and is_int_like(b) and is_int_like(c)
    except Exception:
        h1 = False

    # Conclusion: exists x, y in Z such that ax + by = c (mod m) iff gcd(a, b, m) divides c
    try:
        def to_int(x):
            if isinstance(x, int): return x
            if isinstance(x, sympy.Integer): return int(x)
            if hasattr(x, 'is_integer') and x.is_integer: return int(x)
            if isinstance(x, float) and x.is_integer(): return int(x)
            if isinstance(x, str):
                try:
                    if '.' in x:
                        f = float(x)
                        if f.is_integer(): return int(f)
                    else:
                        return int(x)
                except Exception:
                    pass
            return x

        a_val = to_int(a)
        b_val = to_int(b)
        c_val = to_int(c)
        m_val = to_int(m)

        # Evaluate LHS: exists x, y, k in Z such that a*x + b*y - m*k == c
        if isinstance(m_val, (int, sympy.Integer)):
            g_lhs = sympy.gcd(sympy.gcd(a_val, b_val), m_val)
            lhs_val = (c_val % g_lhs == 0) if g_lhs != 0 else (c_val == 0)
        elif isinstance(m_val, sympy.Rational):
            p, q = m_val.p, m_val.q
            g_lhs = sympy.gcd(sympy.gcd(q*a_val, q*b_val), p)
            lhs_val = ((q*c_val) % g_lhs == 0) if g_lhs != 0 else (c_val == 0)
        else:
            m_rat = sympy.Rational(m_val)
            p, q = m_rat.p, m_rat.q
            g_lhs = sympy.gcd(sympy.gcd(q*a_val, q*b_val), p)
            lhs_val = ((q*c_val) % g_lhs == 0) if g_lhs != 0 else (c_val == 0)

        # Evaluate RHS: gcd(a, b, m) divides c
        g_rhs = sympy.gcd(sympy.gcd(a_val, b_val), m_val)
        if g_rhs == 0:
            rhs_val = (c_val == 0)
        else:
            div = c_val / g_rhs
            if isinstance(div, (int, sympy.Integer)):
                rhs_val = True
            elif hasattr(div, 'is_integer') and div.is_integer:
                rhs_val = True
            elif isinstance(div, sympy.Rational) and div.q == 1:
                rhs_val = True
            elif isinstance(div, float) and div.is_integer():
                rhs_val = True
            else:
                rhs_val = False

        equiv = (lhs_val == rhs_val)
        neg_q = not equiv
    except Exception:
        # If evaluation fails (e.g., gcd of float), the mathematical statement is invalid,
        # hence the conclusion fails.
        neg_q = True

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a, b, and c are integers",
    "¬Q: The equivalence between the congruence solvability and the gcd condition fails"
]

N_HYP = 1
NEG_Q_INDEX = 1