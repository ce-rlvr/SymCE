import sympy
from sympy import symbols
from sympy.polys.domains import QQ, ZZ
from sympy.polys.polytools import groebner

# Top-level setup: named object bindings
x, y, z = symbols('x y z')
R_xy = QQ[x, y]
R_xyz = QQ[x, y, z]

def conditions(witness) -> list[bool]:
    """
    Evaluates the conjecture:
    If R is a UFD and P is a prime ideal, then P is a principal ideal.
    (False because P could have height > 1, e.g., P = <x, y> in Q[x, y])
    """
    try:
        # Witness can be a tuple (ring, generators) or just generators (defaulting to R_xy)
        if isinstance(witness, tuple) and len(witness) == 2:
            ring, gens = witness
        else:
            ring = R_xy
            gens = witness
            
        if not isinstance(gens, (list, tuple, set)):
            gens = [gens]
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        h1_ok = bool(ring.is_UFD)
    except Exception:
        h1_ok = False

    # H_2: P is a prime ideal of R
    try:
        # Attempt to use SymPy's ideal primality if available
        I = ring.ideal(*gens)
        if hasattr(I, 'is_prime'):
            h2_ok = bool(I.is_prime())
        else:
            raise AttributeError
    except Exception:
        try:
            # Fallback for polynomial rings: check sufficient conditions for primality
            gb = groebner(gens, ring.symbols).polys
            if len(gb) == 1:
                # A principal ideal is prime iff its generator is irreducible
                h2_ok = bool(gb[0].is_irreducible)
            else:
                # For monomial ideals, if the reduced Groebner basis consists exactly 
                # of independent linear variables, the ideal is prime.
                h2_ok = all(p.as_expr().is_Symbol for p in gb) and len(gb) <= len(ring.symbols)
        except Exception:
            h2_ok = False

    # ¬Q: P is NOT a principal ideal
    try:
        # An ideal is principal iff its reduced Groebner basis has exactly 1 element
        gb = groebner(gens, ring.symbols).polys
        neg_q_ok = len(gb) > 1
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS: list[str] = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: P is a prime ideal of R",
    "¬Q: P is not a principal ideal"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2