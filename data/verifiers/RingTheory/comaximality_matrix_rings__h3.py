import sympy
import math
import functools
from sympy.abc import x, y, z

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        R, I, J, n = witness
    except Exception:
        return [False, False, False, False]

    # H1: R is a ring
    try:
        h1 = False
        if R in (ZZ, QQ):
            h1 = True
        elif hasattr(R, 'is_Ring') and R.is_Ring:
            h1 = True
        elif hasattr(R, 'has_Field') or hasattr(R, 'domain'):
            h1 = True
    except Exception:
        h1 = False

    # H2: I and J are two-sided ideals of R
    try:
        h2 = False
        if R == ZZ:
            def check_ideal_ZZ(K):
                if isinstance(K, (int, sympy.Integer)): return True
                if isinstance(K, (list, tuple, set)):
                    return all(isinstance(x, (int, sympy.Integer)) for x in K)
                return False
            h2 = check_ideal_ZZ(I) and check_ideal_ZZ(J)
        elif R == QQ:
            def check_ideal_QQ(K):
                if isinstance(K, (int, float, sympy.Integer, sympy.Rational)): return True
                if isinstance(K, (list, tuple, set)): return True
                return False
            h2 = check_ideal_QQ(I) and check_ideal_QQ(J)
        else:
            h2 = isinstance(I, (list, tuple, set)) and isinstance(J, (list, tuple, set))
    except Exception:
        h2 = False

    # H3: n is a positive integer
    try:
        h3 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h3 = False

    # neg_Q: M_n(I) + M_n(J) != M_n(R)
    try:
        neg_q = False
        if R == ZZ:
            def get_gen(K):
                if isinstance(K, (int, sympy.Integer)): return int(K)
                if not K: return 0
                return functools.reduce(math.gcd, [int(x) for x in K])
            i_gen = get_gen(I)
            j_gen = get_gen(J)
            ideal_sum_gen = math.gcd(i_gen, j_gen)
            neg_q = (abs(ideal_sum_gen) != 1)
        elif R == QQ:
            def is_zero(K):
                if isinstance(K, (list, tuple, set)):
                    return all(x == 0 for x in K)
                return K == 0
            neg_q = is_zero(I) and is_zero(J)
        else:
            import sympy.polys
            I_expr = [sympy.sympify(x) for x in I]
            J_expr = [sympy.sympify(x) for x in J]
            gens = I_expr + J_expr
            if not gens:
                neg_q = True
            else:
                gb = sympy.groebner(gens, R.gens, domain=R.domain)
                neg_q = not (len(gb) == 1 and gb[0] == 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I and J are two-sided ideals of R",
    "H_3: n is a positive integer",
    "¬Q: M_n(I) + M_n(J) != M_n(R)"
]

N_HYP = 3
NEG_Q_INDEX = 3