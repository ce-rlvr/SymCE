import sympy
from sympy import eye, zeros, Rational, Integer, Matrix
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

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

def _check_zero(val):
    try:
        if hasattr(val, 'is_zero') and val.is_zero is not None:
            return bool(val.is_zero)
    except Exception:
        pass
    return bool(val == 0)

def _check_eq(a, b):
    try:
        diff = a - b
        if isinstance(diff, sympy.Expr):
            diff = sympy.simplify(diff)
        return _check_zero(diff)
    except Exception:
        return bool(a == b)

def conditions(witness):
    """
    Checks whether the given witness satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        R, u = witness
    else:
        R, u = None, witness

    # H_1: R is an integral domain
    h1_ok = False
    try:
        if R is not None:
            if hasattr(R, 'is_IntegralDomain'):
                h1_ok = bool(R.is_IntegralDomain)
            elif hasattr(R, 'is_domain'):
                h1_ok = bool(R.is_domain)
            else:
                r_str = str(R)
                if r_str.startswith('Zmod') or r_str.startswith('GF') or r_str.startswith('ZZ_'):
                    digits = ''.join(c for c in r_str if c.isdigit())
                    if digits:
                        h1_ok = bool(sympy.isprime(int(digits)))
                    else:
                        h1_ok = True
                else:
                    # Fallback to inferring from u
                    if isinstance(u, sympy.Mod):
                        h1_ok = bool(sympy.isprime(u.args[1]))
                    elif hasattr(u, 'mod'):
                        h1_ok = bool(sympy.isprime(u.mod))
                    elif isinstance(u, sympy.MatrixBase):
                        h1_ok = (u.shape == (1, 1))
                    elif type(u).__module__.startswith('sympy.combinatorics'):
                        h1_ok = False
                    else:
                        h1_ok = True
        else:
            if isinstance(u, sympy.Mod):
                h1_ok = bool(sympy.isprime(u.args[1]))
            elif hasattr(u, 'mod'):
                h1_ok = bool(sympy.isprime(u.mod))
            elif isinstance(u, sympy.MatrixBase):
                h1_ok = (u.shape == (1, 1))
            elif type(u).__module__.startswith('sympy.combinatorics'):
                h1_ok = False
            else:
                h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: u^2 = 1
    h2_ok = False
    try:
        u_sq = u**2
        if isinstance(u, sympy.MatrixBase):
            h2_ok = bool(u_sq == sympy.eye(u.shape[0]))
        elif isinstance(u, sympy.Mod):
            h2_ok = bool(u_sq == sympy.Mod(1, u.args[1]))
        else:
            h2_ok = _check_eq(u_sq, 1)
    except Exception:
        h2_ok = False

    # ¬Q: u != 1 and u != -1
    neg_q = False
    try:
        if isinstance(u, sympy.MatrixBase):
            is_one = bool(u == sympy.eye(u.shape[0]))
            is_minus_one = bool(u == -sympy.eye(u.shape[0]))
        elif isinstance(u, sympy.Mod):
            is_one = bool(u == sympy.Mod(1, u.args[1]))
            is_minus_one = bool(u == sympy.Mod(-1, u.args[1]))
        else:
            is_one = _check_eq(u, 1)
            is_minus_one = _check_eq(u, -1)
        
        neg_q = not (is_one or is_minus_one)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: u^2 = 1",
    "¬Q: u != 1 and u != -1"
]

N_HYP = 2
NEG_Q_INDEX = 2