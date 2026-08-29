import sympy
from sympy import ZZ, QQ, Poly, Symbol
import math

x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "In a Dedekind domain, every ideal is a maximal ideal."
    (The true theorem requires P to be a NON-ZERO PRIME ideal).
    
    Witness can be a tuple (R, P) where R is the domain and P is the ideal generator(s),
    or simply P (in which case R defaults to ZZ).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, P = witness
        else:
            R = ZZ
            P = witness
    except Exception:
        return [False, False]

    # H_1: R is a Dedekind domain
    try:
        h1_ok = False
        if R == ZZ or R is sympy.S.Integers:
            h1_ok = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1_ok = True
        elif hasattr(R, 'is_PID') and R.is_PID:
            h1_ok = True
        elif isinstance(R, sympy.polys.domains.Domain) and R.is_PID:
            h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: P is not a maximal ideal
    try:
        if hasattr(P, 'gens'):
            gens = P.gens
        elif not isinstance(P, (list, tuple, set)):
            gens = [P]
        else:
            gens = list(P)

        is_maximal = False
        if R == ZZ or R is sympy.S.Integers:
            g = 0
            for gen in gens:
                g = math.gcd(g, int(gen))
            is_maximal = sympy.isprime(g)
        elif hasattr(R, 'is_Field') and R.is_Field:
            # In a field, the only maximal ideal is the zero ideal (0)
            is_maximal = all(gen == 0 for gen in gens)
        else:
            # For other PIDs like QQ[x], the ideal is maximal iff the generator is irreducible
            g = gens[0]
            for gen in gens[1:]:
                g = sympy.gcd(g, gen)
            
            if hasattr(R, 'is_irreducible'):
                is_maximal = R.is_irreducible(g)
            else:
                is_maximal = sympy.is_irreducible(g)
                
        neg_q = not is_maximal
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Dedekind domain",
    "¬Q: P is not a maximal ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1