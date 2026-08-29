import sympy
from sympy import *
from sympy.polys import *

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample to the conjecture.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            P = witness.get('P')
            n = witness.get('n')
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, P, n = witness
        else:
            R = getattr(witness, 'R', None)
            P = getattr(witness, 'P', None)
            n = getattr(witness, 'n', None)
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        h1 = False
        if R is not None:
            c = False
            i = True
            if hasattr(R, 'is_commutative'):
                val_c = R.is_commutative
                c = bool(val_c() if callable(val_c) else val_c)
            else:
                # Fallback for standard sympy rings
                if R in [ZZ, QQ] or hasattr(R, 'get_ring'):
                    c = True
            
            if hasattr(R, 'has_identity'):
                val_i = R.has_identity
                i = bool(val_i() if callable(val_i) else val_i)
                
            h1 = c and i
    except Exception:
        h1 = False

    # H_2: P is a prime ideal in R
    try:
        h2 = False
        if P is not None:
            if hasattr(P, 'is_prime'):
                val = P.is_prime
                h2 = bool(val() if callable(val) else val)
            elif hasattr(P, 'is_prime_ideal'):
                val = P.is_prime_ideal
                h2 = bool(val() if callable(val) else val)
    except Exception:
        h2 = False

    # H_3: n is a positive integer
    try:
        h3 = isinstance(n, int) and n > 0
    except Exception:
        h3 = False

    # neg_Q: The symbolic power P^(n) is not a P-primary ideal
    try:
        neg_q = False
        if P is not None and hasattr(P, 'symbolic_power'):
            Pn = P.symbolic_power(n)
            if hasattr(Pn, 'is_primary'):
                val = Pn.is_primary
                try:
                    is_prim = val(P) if callable(val) else val
                except TypeError:
                    is_prim = val() if callable(val) else val
                neg_q = not bool(is_prim)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: P is a prime ideal in R",
    "H_3: n is a positive integer",
    "¬Q: The symbolic power P^(n) is not a P-primary ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3