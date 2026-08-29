import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The equivalence fails (R is not a UFD, but every height 1 prime is principal)"
]

def get_ring_properties(witness):
    """
    Extracts or deduces the ring properties from the witness.
    Returns a tuple: (is_integral_domain, is_ufd, height_1_primes_principal)
    """
    is_id = False
    is_ufd = False
    h1_prin = False

    # 1. Tuple format
    if isinstance(witness, tuple) and len(witness) == 3:
        if all(isinstance(val, bool) for val in witness):
            return witness

    # 2. String format (known counterexamples and non-counterexamples)
    if isinstance(witness, str):
        w_lower = witness.lower()
        if "entire" in w_lower or "h(c)" in w_lower:
            return True, False, True
        if "valuation" in w_lower and ("dense" in w_lower or "q" in w_lower or "r" in w_lower or "rational" in w_lower or "real" in w_lower):
            return True, False, True
        if "z[sqrt(-5)]" in w_lower or "z[i*sqrt(5)]" in w_lower:
            return True, False, False
        if "z+x*q[x]" in w_lower:
            return True, False, False
        if w_lower in ["z", "q", "z[x]", "q[x]"]:
            return True, True, True

    # 3. Dictionary format
    if isinstance(witness, dict):
        id_val = witness.get('is_integral_domain', witness.get('is_Domain', witness.get('is_domain')))
        if isinstance(id_val, bool): 
            is_id = id_val
        
        ufd_val = witness.get('is_ufd', witness.get('is_UFD'))
        if isinstance(ufd_val, bool): 
            is_ufd = ufd_val
        
        h1_val = witness.get('every_height_1_prime_is_principal', witness.get('height_1_primes_principal', witness.get('h1_primes_principal')))
        if isinstance(h1_val, bool): 
            h1_prin = h1_val
        elif is_ufd: 
            h1_prin = True
            
        return is_id, is_ufd, h1_prin

    # 4. Object attributes format (e.g., SymPy domains or custom classes)
    def get_bool_attr(obj, attrs):
        for attr in attrs:
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if callable(val):
                    try:
                        val = val()
                    except Exception:
                        continue
                if isinstance(val, bool):
                    return val
        return None

    id_val = get_bool_attr(witness, ['is_integral_domain', 'is_Domain', 'is_domain'])
    if id_val is not None:
        is_id = id_val

    ufd_val = get_bool_attr(witness, ['is_ufd', 'is_UFD'])
    if ufd_val is not None:
        is_ufd = ufd_val

    h1_val = get_bool_attr(witness, ['every_height_1_prime_is_principal', 'height_1_primes_principal', 'h1_primes_principal'])
    if h1_val is not None:
        h1_prin = h1_val
    elif is_ufd:
        # In any integral domain, if it is a UFD, every height 1 prime is principal.
        h1_prin = True

    return is_id, is_ufd, h1_prin

def conditions(witness) -> list[bool]:
    try:
        is_id, is_ufd, h1_prin = get_ring_properties(witness)
    except Exception:
        return [False, False]

    try:
        h1_ok = bool(is_id)
    except Exception:
        h1_ok = False

    try:
        # The conclusion Q is: R is a UFD iff every height 1 prime is principal.
        # This means Q is equivalent to (is_ufd == h1_prin).
        # The negation ¬Q is true when the equivalence fails.
        neg_q_ok = bool(is_ufd != h1_prin)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]