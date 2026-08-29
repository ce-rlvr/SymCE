import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# We use integers to represent ideals in the commutative ring Z.
# For example, the integer m represents the ideal mZ.

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the false conjecture.
    The witness can be an integer m (representing ideal mZ in Z) 
    or a tuple (m, p) representing ideals mZ and pZ.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            try:
                m = int(witness[0])
                p = int(witness[1])
            except Exception:
                m = None
                p = None
        else:
            try:
                m = int(witness)
                if m > 0:
                    if m == 1:
                        p = 1
                    else:
                        p = 1
                        for f in sympy.primefactors(m):
                            p *= f
                else:
                    m = None
                    p = None
            except Exception:
                m = None
                p = None

        # H_1: R is a commutative ring
        # We interpret the witness as ideals in Z, which is a commutative ring.
        # We just need m and p to be valid positive integers.
        try:
            h1 = (m is not None) and (p is not None) and m > 0 and p > 0
        except Exception:
            h1 = False

        # H_2: P = \sqrt{Q} is the radical of Q
        try:
            if m is None or p is None:
                h2 = False
            else:
                if m == 1:
                    rad_m = 1
                else:
                    rad_m = 1
                    for f in sympy.primefactors(m):
                        rad_m *= f
                h2 = (p == rad_m)
        except Exception:
            h2 = False

        # ¬Q: P is not the unique minimal prime ideal containing Q
        try:
            if m is None or p is None:
                neg_q = False
            else:
                if m == 1:
                    # Z has no prime ideals containing Z
                    is_unique = False
                else:
                    factors = sympy.primefactors(m)
                    # In Z, the minimal prime ideals containing mZ are exactly pZ for p in prime factors of m.
                    # So there is a unique minimal prime iff m has exactly 1 prime factor.
                    # And P is that unique minimal prime iff p is that prime factor.
                    is_unique = (len(factors) == 1 and p == factors[0])
                neg_q = not is_unique
        except Exception:
            neg_q = False

        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P = \\sqrt{Q} is the radical of Q",
    "¬Q: P is not the unique minimal prime ideal containing Q"
]

N_HYP = 2
NEG_Q_INDEX = 2