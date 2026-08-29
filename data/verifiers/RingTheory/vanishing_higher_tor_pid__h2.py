import sympy
from sympy import eye, zeros, Rational, Integer, ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_global_dimension(ring):
    """
    Helper function to compute the global dimension of a sympy domain.
    Returns 0 for fields, 1 for PIDs, and recursively adds 1 for each
    polynomial variable. Returns infinity for unknown rings.
    """
    try:
        if getattr(ring, 'is_Field', False):
            return 0
        if hasattr(ring, 'dom') and hasattr(ring, 'symbols'):
            return get_global_dimension(ring.dom) + len(ring.symbols)
        if getattr(ring, 'is_PID', False):
            return 1
        return float('inf')
    except Exception:
        return float('inf')

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the given witness.
    The witness is expected to be a tuple (R, n) where R is a sympy domain
    and n is an integer.
    """
    R = None
    n = None
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, n = witness
        elif isinstance(witness, dict):
            R = witness.get('R')
            n = witness.get('n')
        else:
            R = witness
    except Exception:
        pass

    # H_1: Let R be a principal ideal domain
    try:
        h1 = bool(getattr(R, 'is_PID', False))
    except Exception:
        h1 = False

    # H_2: Let n >= 2 be an integer
    try:
        if isinstance(n, (int, sympy.Integer)):
            h2 = int(n) >= 2
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The Tor functor Tor_n^R(M, N) is NOT identically zero
    # Tor_n is identically zero iff the global dimension of R is strictly less than n.
    # Therefore, it is NOT identically zero iff global_dimension(R) >= n.
    try:
        if n is None or not isinstance(n, (int, sympy.Integer)):
            neg_q = False
        else:
            gl_dim = get_global_dimension(R)
            neg_q = bool(gl_dim >= int(n))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: n >= 2 is an integer",
    "¬Q: The Tor functor Tor_n^R(M, N) is NOT identically zero"
]

N_HYP = 2
NEG_Q_INDEX = 2