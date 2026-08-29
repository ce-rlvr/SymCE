import sympy
from sympy import eye
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: a and b are elements of R",
    "H_2: 1 - ab is a unit in R",
    "¬Q: 1 - ba is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The dropped hypothesis is that R is a ring (i.e., closed under its operations).
    A valid counterexample can be a tuple (R, a, b) where R is a subset of a ring,
    or just (a, b) if they belong to a non-associative structure.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, a, b = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            a, b = witness
            R = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def get_one(x):
        if hasattr(x, 'rows') and hasattr(x, 'cols') and x.rows == x.cols:
            return sympy.eye(x.rows)
        return 1

    try:
        ab = a * b
        one_ab = get_one(ab)
        u = one_ab - ab
    except Exception:
        u = None
        one_ab = None

    try:
        ba = b * a
        one_ba = get_one(ba)
        v = one_ba - ba
    except Exception:
        v = None
        one_ba = None

    if R is not None:
        # H1: a and b are elements of R
        try:
            h1 = False
            if hasattr(R, '__contains__') and not isinstance(R, list):
                h1 = (a in R) and (b in R)
            else:
                a_in_R = any(a == x for x in R)
                b_in_R = any(b == x for x in R)
                h1 = bool(a_in_R and b_in_R)
        except Exception:
            h1 = False

        # H2: 1 - ab is a unit in R
        try:
            h2 = False
            if u is not None:
                u_in_R = any(u == x for x in R) if not hasattr(R, '__contains__') or isinstance(R, list) else (u in R)
                if u_in_R:
                    for x in R:
                        try:
                            if (u * x == one_ab) and (x * u == one_ab):
                                h2 = True
                                break
                        except Exception:
                            continue
        except Exception:
            h2 = False

        # ¬Q: 1 - ba is NOT a unit in R
        try:
            q = False
            if v is not None:
                v_in_R = any(v == x for x in R) if not hasattr(R, '__contains__') or isinstance(R, list) else (v in R)
                if v_in_R:
                    for y in R:
                        try:
                            if (v * y == one_ba) and (y * v == one_ba):
                                q = True
                                break
                        except Exception:
                            continue
            neg_q = not q
        except Exception:
            neg_q = False

    else:
        # R is implicit
        h1 = True
        
        try:
            h2 = False
            if u is not None:
                if isinstance(u, int) or (hasattr(u, 'is_Integer') and u.is_Integer):
                    h2 = (u == 1 or u == -1)
                elif hasattr(u, 'is_Rational') and u.is_Rational:
                    h2 = (u != 0)
                elif hasattr(u, 'is_unit'):
                    h2 = bool(u.is_unit)
                elif hasattr(u, 'inv'):
                    _ = u.inv()
                    h2 = True
                else:
                    _ = one_ab / u
                    h2 = True
        except Exception:
            h2 = False

        try:
            q = False
            if v is not None:
                if isinstance(v, int) or (hasattr(v, 'is_Integer') and v.is_Integer):
                    q = (v == 1 or v == -1)
                elif hasattr(v, 'is_Rational') and v.is_Rational:
                    q = (v != 0)
                elif hasattr(v, 'is_unit'):
                    q = bool(v.is_unit)
                elif hasattr(v, 'inv'):
                    _ = v.inv()
                    q = True
                else:
                    _ = one_ba / v
                    q = True
            neg_q = not q
        except Exception:
            neg_q = True

    return [h1, h2, neg_q]