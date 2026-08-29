import sympy
import math

ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide the ring R, and elements a, b, d.
    It can be a dictionary {'R': R, 'a': a, 'b': b, 'd': d} or a tuple (R, a, b, d) or (a, b, d).
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R', ZZ)
            a = witness.get('a')
            b = witness.get('b')
            d = witness.get('d')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                R, a, b, d = witness
            elif len(witness) == 3:
                R = ZZ
                a, b, d = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if a is None or b is None or d is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a principal ideal domain
    try:
        h1 = False
        if R in (ZZ, sympy.ZZ):
            h1 = True
        else:
            if hasattr(R, 'is_PID') and R.is_PID:
                h1 = True
            elif hasattr(R, 'is_Poly') and getattr(R, 'is_Poly'):
                if hasattr(R, 'domain') and getattr(R.domain, 'is_Field'):
                    if hasattr(R, 'gens') and len(R.gens) == 1:
                        h1 = True
            elif isinstance(R, sympy.polys.domains.principalidealdomain.PrincipalIdealDomain):
                h1 = True
    except Exception:
        h1 = False

    # H2: a and b are non-zero elements of R
    try:
        h2 = False
        def in_R(val, ring):
            if ring in (ZZ, sympy.ZZ):
                return isinstance(val, (int, sympy.Integer))
            try:
                return val in ring
            except Exception:
                return False

        if in_R(a, R) and in_R(b, R) and a != 0 and b != 0:
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: Hom_R(R/<a>, R/<b>) is NOT isomorphic to R/<d>
    # For a PID, Hom_R(R/<a>, R/<b>) is isomorphic to R/<gcd(a,b)>.
    # Thus, it is isomorphic to R/<d> iff gcd(a,b) and d are associates.
    try:
        neg_q = False
        if R in (ZZ, sympy.ZZ):
            if not isinstance(d, (int, sympy.Integer)):
                neg_q = True
            else:
                g = math.gcd(int(a), int(b))
                if abs(int(g)) != abs(int(d)):
                    neg_q = True
        else:
            if not in_R(d, R):
                neg_q = True
            else:
                g = sympy.gcd(a, b)
                g_expr = sympy.sympify(g)
                d_expr = sympy.sympify(d)
                if g_expr == 0 and d_expr == 0:
                    are_assoc = True
                elif g_expr == 0 or d_expr == 0:
                    are_assoc = False
                else:
                    try:
                        q1, r1 = sympy.div(g_expr, d_expr, domain=R)
                        q2, r2 = sympy.div(d_expr, g_expr, domain=R)
                    except Exception:
                        q1, r1 = sympy.div(g_expr, d_expr)
                        q2, r2 = sympy.div(d_expr, g_expr)
                    are_assoc = (r1 == 0 and r2 == 0)
                if not are_assoc:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: a and b are non-zero elements of R",
    "¬Q: Hom_R(R/<a>, R/<b>) is not isomorphic to R/<d>"
]

N_HYP = 2
NEG_Q_INDEX = 2