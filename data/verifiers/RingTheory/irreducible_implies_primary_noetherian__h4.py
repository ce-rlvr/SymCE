import sympy
from sympy.ntheory import factorint
import math

Z = sympy.S.Integers
ZZ = sympy.S.Integers

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture:
    "In a Noetherian ring, every proper ideal is primary."
    
    We evaluate the witness as an ideal in the ring of integers Z.
    The witness can be an integer n (representing the ideal nZ),
    or a collection containing the generator.
    """
    def extract_integer(obj):
        if hasattr(obj, 'gens'):
            try:
                gens = obj.gens
                if len(gens) > 0:
                    val = int(gens[0])
                    for g in gens[1:]:
                        val = math.gcd(val, int(g))
                    return val
                else:
                    return 0
            except Exception:
                pass
        try:
            if isinstance(obj, str):
                return int(obj)
            # Only cast if it's a direct numeric type to avoid weird SymPy expression casts
            if hasattr(obj, '__int__'):
                return int(obj)
        except (ValueError, TypeError):
            pass
        
        if isinstance(obj, (tuple, list, set)):
            for item in obj:
                val = extract_integer(item)
                if val is not None:
                    return val
                    
        if isinstance(obj, dict):
            for item in obj.values():
                val = extract_integer(item)
                if val is not None:
                    return val
                    
        return None

    try:
        n = extract_integer(witness)
        if n is None:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring with identity
    # The ring of integers Z is a commutative ring with identity.
    h1 = True

    # H2: R is a Noetherian ring
    # Z is a Principal Ideal Domain, hence Noetherian.
    h2 = True

    # H3: I is a proper ideal of R
    # In Z, the ideal nZ is proper if and only if n != 1 and n != -1.
    try:
        h3 = abs(n) != 1
    except Exception:
        h3 = False

    # ¬Q: I is not a primary ideal
    # In Z, nZ is primary if and only if n = 0 or n = p^k for some prime p and k >= 1.
    try:
        if n == 0:
            neg_q = False
        elif abs(n) == 1:
            neg_q = True  # 1Z is not proper, hence not primary by definition
        else:
            factors = factorint(abs(n))
            neg_q = len(factors) > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "H_3: I is a proper ideal of R",
    "¬Q: I is not a primary ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3