import sympy
from sympy import ZZ, QQ
from sympy.polys.domains import Domain

# Standard bindings for Ring Theory / Linear Algebra
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, x) where R is a ring (e.g., sympy.ZZ) 
    and x is an element of R.
    """
    try:
        R, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: R is a commutative ring
    try:
        h1 = False
        if isinstance(R, Domain):
            h1 = True
        elif hasattr(R, 'is_commutative') and hasattr(R, 'is_ring'):
            h1 = bool(R.is_commutative and R.is_ring)
        elif hasattr(R, 'zero') and hasattr(R, 'one') and hasattr(R, '__contains__'):
            h1 = True
    except Exception:
        h1 = False

    # H_2: R has a multiplicative identity
    try:
        h2 = hasattr(R, 'one') and R.one is not None
    except Exception:
        h2 = False

    # H_3: x is a non-zero element of R
    try:
        h3 = bool((x in R) and (x != R.zero))
    except Exception:
        h3 = False

    # neg_Q: x is neither a unit nor a zero divisor in R
    try:
        is_unit = False
        if hasattr(R, 'is_unit'):
            is_unit = R.is_unit(x)
        else:
            try:
                q = R.exquo(R.one, x)
                if hasattr(R, 'mul'):
                    is_unit = bool(R.mul(q, x) == R.one)
                else:
                    is_unit = bool(q * x == R.one)
            except Exception:
                try:
                    is_unit = bool((sympy.S(1) / x) in R)
                except Exception:
                    is_unit = False

        is_zero_divisor = False
        if hasattr(R, 'is_zero_divisor'):
            is_zero_divisor = R.is_zero_divisor(x)
        elif hasattr(R, 'zero_divisors'):
            zd = R.zero_divisors() if callable(R.zero_divisors) else R.zero_divisors
            is_zero_divisor = bool(x in zd)
        elif isinstance(R, Domain):
            # SymPy domains are integral domains; non-zero elements are not zero divisors
            is_zero_divisor = bool(x == R.zero)
        else:
            is_zero_divisor = False

        neg_q = not (is_unit or is_zero_divisor)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "H_3: x is a non-zero element of R",
    "¬Q: x is neither a unit nor a zero divisor in R"
]

N_HYP = 3
NEG_Q_INDEX = 3