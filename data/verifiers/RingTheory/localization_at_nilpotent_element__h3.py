import sympy
from sympy import ZZ, QQ, S
from sympy.polys.rings import PolyRing

# Top-level setup
# No specific named bindings required for this domain.
# ZZ and QQ are imported and can be used directly.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, x) where R is a ring and x is an element.
    For convenience, R can be represented as an integer n >= 0 (meaning Z/nZ),
    or a SymPy ring like ZZ, QQ, or a PolyRing.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        n, x = witness
    except Exception:
        return [False, False, False]
    
    # H1: R is a commutative ring with identity
    try:
        if isinstance(n, int) and n >= 0:
            h1 = True
        elif hasattr(n, 'mod') and isinstance(n.mod, int):
            h1 = True
        elif n in [ZZ, QQ, S.Reals, S.Complexes]:
            h1 = True
        elif isinstance(n, PolyRing):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: x is an element of R
    try:
        if isinstance(n, int) and n >= 0:
            h2 = isinstance(x, int) or (hasattr(x, 'is_integer') and x.is_integer)
        elif hasattr(n, 'mod') and isinstance(n.mod, int):
            h2 = isinstance(x, int) or (hasattr(x, 'is_integer') and x.is_integer) or (x in n)
        elif n in [ZZ, QQ, S.Reals, S.Complexes]:
            h2 = x in n
        elif isinstance(n, PolyRing):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The localization of R at {1, x, x^2, ...} is NOT the zero ring
    # This is mathematically equivalent to: x is NOT nilpotent in R
    try:
        if isinstance(n, int) and n >= 0:
            modulus = n
        elif hasattr(n, 'mod') and isinstance(n.mod, int):
            modulus = n.mod
        else:
            modulus = None

        if modulus is not None:
            if modulus == 0:
                try:
                    if hasattr(x, 'val'):
                        val = int(x.val)
                    else:
                        val = int(x)
                    is_nilp = (val == 0)
                except Exception:
                    is_nilp = (x == 0)
            elif modulus == 1:
                is_nilp = True
            else:
                from sympy.ntheory import factorint
                factors = factorint(modulus)
                try:
                    if hasattr(x, 'val'):
                        val = int(x.val)
                    else:
                        val = int(x)
                except Exception:
                    val = 1 # fallback, makes it not nilpotent
                is_nilp = all(val % p == 0 for p in factors.keys())
        elif n in [ZZ, QQ, S.Reals, S.Complexes]:
            is_nilp = (x == 0)
        elif isinstance(n, PolyRing):
            is_nilp = (x == 0 or (hasattr(n, 'zero') and x == n.zero))
        else:
            is_nilp = True # Fallback, makes neg_q False
            
        neg_q = not is_nilp
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: x is an element of R",
    "¬Q: The localization of R at {1, x, x^2, ...} is not the zero ring (x is not nilpotent)"
]

N_HYP = 2
NEG_Q_INDEX = 2