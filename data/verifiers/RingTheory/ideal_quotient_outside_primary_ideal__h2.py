import sympy
from sympy import gcd
from sympy.ntheory import factorint, isprime

# Top-level setup for potential witness evaluation
# We restrict our verification to the ring of integers Z, 
# which is a commutative ring with identity.
ZZ = sympy.S.Integers

def extract_int(v):
    """Helper to extract an integer from a singleton list/tuple/set or SymPy object."""
    if isinstance(v, (list, tuple, set)) and len(v) == 1:
        v = list(v)[0]
    return int(v)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    The witness is expected to represent ideals in Z and an element x.
    Format: (Q_gen, P_gen, x) or (R, Q_gen, P_gen, x) or a dict with keys 'Q', 'P', 'x'.
    """
    try:
        if isinstance(witness, dict):
            q = witness.get('Q', witness.get('q'))
            p = witness.get('P', witness.get('p'))
            x = witness.get('x')
            if q is None or p is None or x is None:
                return [False, False, False]
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                q, p, x = witness
            elif len(witness) == 4:
                _, q, p, x = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        q = extract_int(q)
        p = extract_int(p)
        x = extract_int(x)
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    # By successfully parsing the witness into integers, we are working in Z,
    # which is a commutative ring with identity.
    h1 = True
    
    # H_2: x is an element of R such that x ∉ Q
    # In Z, x ∉ qZ means x is not a multiple of q.
    try:
        if q == 0:
            h2 = (x != 0)
        else:
            h2 = (x % q != 0)
    except Exception:
        h2 = False
        
    # ¬Q: The ideal quotient (Q : x) is NOT a P-primary ideal
    try:
        # Compute the generator of the ideal quotient (qZ : x) in Z
        if q == 0:
            if x == 0:
                quot = 1  # (0 : 0) = Z = 1*Z
            else:
                quot = 0  # (0 : x) = 0*Z
        else:
            quot = abs(q) // gcd(abs(q), abs(x))
            
        def is_P_primary(m, p_gen):
            """Checks if the ideal mZ is p_gen*Z - primary in Z."""
            m = abs(m)
            p_gen = abs(p_gen)
            if m == 0:
                return p_gen == 0
            if m == 1:
                return False  # Z is not a proper primary ideal
            if not isprime(p_gen):
                return False  # P must be a prime ideal
            factors = factorint(m)
            # mZ is pZ-primary iff m = p^k for some k >= 1
            return list(factors.keys()) == [p_gen]
            
        is_primary = is_P_primary(quot, p)
        neg_q = not is_primary
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: x is an element of R such that x ∉ Q",
    "¬Q: The ideal quotient (Q : x) is not a P-primary ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2