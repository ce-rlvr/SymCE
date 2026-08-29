import math
import sympy
from sympy import Symbol

# Top-level setup for witness expressions
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: a and b are non-zero elements of R",
    "¬Q: R/<a> ⊗ R/<b> is not isomorphic to R/<d>"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    a, b, d = None, None, None
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            d = witness.get('d')
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                a, b, d = witness
            elif len(witness) == 4:
                _, a, b, d = witness
    except Exception:
        pass

    # H_1: R is a principal ideal domain
    # We verify that the elements belong to Z or a univariate polynomial ring (which are PIDs or treated as such here)
    try:
        valid_types = (int, sympy.Integer, sympy.Expr)
        if not (isinstance(a, valid_types) and isinstance(b, valid_types) and isinstance(d, valid_types)):
            h1 = False
        elif isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)) and isinstance(d, (int, sympy.Integer)):
            h1 = True
        else:
            vars_a = getattr(a, 'free_symbols', set())
            vars_b = getattr(b, 'free_symbols', set())
            vars_d = getattr(d, 'free_symbols', set())
            all_vars = vars_a | vars_b | vars_d
            h1 = len(all_vars) <= 1
    except Exception:
        h1 = False

    # H_2: a and b are non-zero elements of R
    try:
        h2 = (a != 0) and (b != 0)
    except Exception:
        h2 = False

    # ¬Q: R/<a> ⊗ R/<b> is not isomorphic to R/<d>
    # R/<a> ⊗ R/<b> is isomorphic to R/<gcd(a,b)>.
    # Thus, it is NOT isomorphic to R/<d> if gcd(a,b) and d do not generate the same ideal (i.e., are not associates).
    try:
        if a is None or b is None or d is None:
            neg_q = False
        else:
            g = sympy.gcd(a, b)
            
            def is_associate(u, v):
                if u == 0 and v == 0:
                    return True
                if u == 0 or v == 0:
                    return False
                if isinstance(u, (int, sympy.Integer)) and isinstance(v, (int, sympy.Integer)):
                    return abs(u) == abs(v)
                q1, r1 = sympy.div(u, v)
                q2, r2 = sympy.div(v, u)
                return r1 == 0 and r2 == 0
                
            neg_q = not is_associate(g, d)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]