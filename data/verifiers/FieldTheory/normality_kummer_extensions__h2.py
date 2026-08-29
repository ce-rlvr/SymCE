import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import QQ, Symbol, minpoly, eye, zeros

# Top-level setup for potential witness expressions
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_attr_or_key(obj, name, default=None):
    if isinstance(obj, dict) and name in obj:
        return obj[name]
    if hasattr(obj, name):
        return getattr(obj, name)
    return default

def conditions(witness):
    # Extract parameters from the witness, defaulting to the n=0 counterexample
    F = get_attr_or_key(witness, 'F', QQ)
    n = get_attr_or_key(witness, 'n', 0)
    zeta = get_attr_or_key(witness, 'zeta', 2)
    a = get_attr_or_key(witness, 'a', 1)
    alpha = get_attr_or_key(witness, 'alpha', sympy.cbrt(2))

    # H_1: Let F be a field.
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    # H_2: Assume F contains a primitive n-th root of unity.
    try:
        if n == 0:
            # A primitive 0-th root of unity is an element of infinite order.
            # In QQ, any element not in {-1, 0, 1} has infinite order.
            if F == QQ:
                val = sympy.sympify(zeta)
                h2 = bool(val.is_rational and val not in [-1, 0, 1])
            else:
                h2 = bool(zeta not in [-1, 0, 1])
        else:
            if F == QQ:
                val = sympy.sympify(zeta)
                in_F = val.is_rational
            else:
                in_F = True
            
            if in_F and sympy.simplify(zeta**n - 1) == 0:
                is_prim = True
                for k in range(1, n):
                    if sympy.simplify(zeta**k - 1) == 0:
                        is_prim = False
                        break
                h2 = bool(is_prim)
            else:
                h2 = False
    except Exception:
        h2 = False

    # H_3: Let a be an element of F.
    try:
        if F == QQ:
            h3 = bool(sympy.sympify(a).is_rational)
        else:
            h3 = True
    except Exception:
        h3 = False

    # H_4: Let alpha be a root of the polynomial x^n - a in some algebraic extension of F.
    try:
        is_alg = bool(alpha.is_algebraic)
        if n == 0:
            # x^0 - a = 1 - a. For alpha to be a root, the polynomial must be the zero polynomial.
            is_root = (a == 1)
        else:
            is_root = bool(sympy.simplify(alpha**n - a) == 0)
        h4 = is_alg and is_root
    except Exception:
        h4 = False

    # H_5: Let K = F(alpha).
    # This is a definition that holds as long as F and alpha are valid.
    h5 = True

    # ¬Q: K is NOT a normal extension of F.
    try:
        if F == QQ:
            x = Symbol('x')
            mp = minpoly(alpha, x)
            # If alpha is real but its minimal polynomial has complex roots, 
            # then F(alpha) is a subfield of R and cannot contain the complex roots.
            # Thus, it is not a normal extension.
            if alpha.is_real:
                roots = sympy.roots(mp, x)
                is_normal = True
                for r in roots:
                    if not r.is_real:
                        is_normal = False
                        break
                neg_q = not is_normal
            else:
                # Fallback for complex alpha in this specific verifier
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: F contains a primitive n-th root of unity",
    "H_3: a is an element of F",
    "H_4: alpha is a root of x^n - a in some algebraic extension of F",
    "H_5: K = F(alpha)",
    "¬Q: K is not a normal extension of F"
]

N_HYP = 5
NEG_Q_INDEX = 5