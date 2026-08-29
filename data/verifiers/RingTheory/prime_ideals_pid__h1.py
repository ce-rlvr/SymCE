import sympy
from sympy import symbols
from sympy.polys.domains import QQ, ZZ
from sympy.ntheory import isprime

# Top-level setup
x, y, z = symbols('x y z')
R_xy = QQ[x, y]
R_xyz = QQ[x, y, z]
R_zx = ZZ[x]
R_zxy = ZZ[x, y]

def conditions(witness) -> list[bool]:
    try:
        # Parse witness: can be a tuple (Ring, generators) or an Ideal object
        if isinstance(witness, tuple) and len(witness) == 2:
            R, gens = witness
            if hasattr(R, 'ideal'):
                P = R.ideal(*gens)
            else:
                P = witness
        else:
            P = witness
            R = P.ring
    except Exception:
        return [False, False]

    # H_1: P is a non-zero prime ideal of R
    try:
        is_zero = P.is_zero()
    except Exception:
        is_zero = None

    if is_zero is None:
        is_zero = False
        try:
            is_zero = all(g == 0 for g in P.gens)
        except Exception:
            pass

    try:
        is_prime = P.is_prime()
    except Exception:
        is_prime = None

    # Fallback for prime check if SymPy's ideal.is_prime() is not implemented or returns False
    if not is_prime:
        try:
            gens = P.gens
            if len(gens) == 1:
                expr = gens[0].as_expr()
                if expr.is_Integer and expr.is_number:
                    is_prime = isprime(int(expr))
                else:
                    domain = getattr(R, 'domain', None)
                    if domain:
                        is_prime = expr.is_irreducible
                    else:
                        is_prime = expr.is_irreducible
        except Exception:
            pass

    if is_prime is None:
        is_prime = False

    h1 = (not is_zero) and is_prime

    # ¬Q: P is NOT a maximal ideal of R
    try:
        is_maximal = P.is_maximal()
    except Exception:
        is_maximal = None

    # Fallback for maximal check using Krull's Principal Ideal Theorem
    try:
        gens = P.gens
        if hasattr(R, 'domain') and hasattr(R, 'gens'):
            if R.domain == QQ and len(R.gens) >= 2:
                if len(gens) < len(R.gens):
                    is_maximal = False
            elif R.domain == ZZ and len(R.gens) >= 1:
                if len(gens) < len(R.gens) + 1:
                    is_maximal = False
    except Exception:
        pass

    if is_maximal is None:
        is_maximal = True

    neg_q = not is_maximal

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: P is a non-zero prime ideal of R",
    "¬Q: P is not a maximal ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1