import math
import sympy
from sympy import ZZ, QQ, GF
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture:
    "If M_1 and M_2 are maximal ideals of a commutative ring R with identity, then M_1 + M_2 = R."
    
    Expected witness format: (R, M1_gens, M2_gens)
    where R is a SymPy domain (e.g., ZZ, QQ, or GF(p)),
    and M1_gens, M2_gens are lists of generators for the ideals (or single elements).
    """
    try:
        R, M1, M2 = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a commutative ring with identity
    try:
        h1 = False
        if R in (ZZ, QQ):
            h1 = True
        elif hasattr(R, 'is_FiniteField') and R.is_FiniteField:
            h1 = True
    except Exception:
        h1 = False

    # H_2: M_1 and M_2 are maximal ideals of R
    try:
        def check_maximal(domain, gens):
            if not isinstance(gens, (list, tuple, set)):
                gens = [gens]
            if domain == ZZ:
                g = 0
                for gen in gens:
                    g = math.gcd(g, int(gen))
                return sympy.isprime(g)
            if domain == QQ or (hasattr(domain, 'is_FiniteField') and domain.is_FiniteField):
                # In a field, the only maximal ideal is the zero ideal {0}
                for gen in gens:
                    if domain == QQ:
                        if gen != 0: 
                            return False
                    else:
                        if int(gen) % domain.mod != 0: 
                            return False
                return True
            return False
        
        h2 = bool(check_maximal(R, M1) and check_maximal(R, M2))
    except Exception:
        h2 = False

    # ¬Q: M_1 + M_2 is not equal to R
    try:
        def check_whole_ring(domain, gens1, gens2):
            if not isinstance(gens1, (list, tuple, set)):
                gens1 = [gens1]
            if not isinstance(gens2, (list, tuple, set)):
                gens2 = [gens2]
            if domain == ZZ:
                g = 0
                for gen in list(gens1) + list(gens2):
                    g = math.gcd(g, int(gen))
                return g == 1 or g == -1
            if domain == QQ or (hasattr(domain, 'is_FiniteField') and domain.is_FiniteField):
                # In a field, any non-zero element generates the whole ring
                for gen in list(gens1) + list(gens2):
                    if domain == QQ:
                        if gen != 0: 
                            return True
                    else:
                        if int(gen) % domain.mod != 0: 
                            return True
                return False
            return False
        
        neg_q = not check_whole_ring(R, M1, M2)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M_1 and M_2 are maximal ideals of R",
    "¬Q: M_1 + M_2 is not equal to R"
]

N_HYP = 2
NEG_Q_INDEX = 2