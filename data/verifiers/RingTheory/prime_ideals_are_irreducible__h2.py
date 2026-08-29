import math
import sympy
from sympy.ntheory import factorint
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
from sympy import S

# Top-level setup for potential witness references
Z = S.Integers
ZZ = S.Integers
Q = S.Rationals
QQ = S.Rationals
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract_ideal_number(s):
    """Extracts the integer generator from a string representation of an ideal."""
    s_str = str(s)
    s_lower = s_str.lower()
    
    # Check if it's a simple ideal representation (e.g., "6Z", "<6>", "Ideal(6)")
    cleaned = s_lower
    for word in ['ideal', 'z', '(', ')', '<', '>', ' ', '_', ',']:
        cleaned = cleaned.replace(word, '')
    if not cleaned.isdigit() and cleaned != '':
        return None
        
    # Extract the first contiguous sequence of digits
    digits = []
    for char in s_str:
        if char.isdigit():
            digits.append(char)
        elif digits:
            break
    if digits:
        return int("".join(digits))
    return None

def get_preimage_generator(witness):
    """
    Attempts to interpret the witness as an ideal in Z or Z_n,
    and returns the non-negative integer generator of its preimage in Z.
    """
    if isinstance(witness, int):
        return witness
    if hasattr(witness, 'is_Integer') and witness.is_Integer:
        return int(witness)
        
    if isinstance(witness, str):
        num = extract_ideal_number(witness)
        if num is not None:
            return num
            
    if isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            ring, ideal = witness
            
            d = None
            if isinstance(ideal, int):
                d = ideal
            elif hasattr(ideal, 'is_Integer') and ideal.is_Integer:
                d = int(ideal)
            elif isinstance(ideal, str) or hasattr(ideal, '__str__'):
                d = extract_ideal_number(str(ideal))
                    
            n = None
            if isinstance(ring, int):
                n = ring
            elif hasattr(ring, 'is_Integer') and ring.is_Integer:
                n = int(ring)
            elif isinstance(ring, str) or hasattr(ring, '__str__'):
                ring_str = str(ring).lower()
                if 'z' in ring_str or 'mod' in ring_str:
                    digits = []
                    for char in ring_str:
                        if char.isdigit():
                            digits.append(char)
                        elif digits:
                            break
                    if digits:
                        n = int("".join(digits))
                    
            if d is not None:
                if d == 0 and n is not None:
                    return n
                if n is not None and n != 0:
                    return math.gcd(d, n)
                return d
                
        # Fallback for tuples not matching (ring, ideal)
        ideal = witness[-1]
        if isinstance(ideal, int):
            return ideal
        if hasattr(ideal, 'is_Integer') and ideal.is_Integer:
            return int(ideal)
        if isinstance(ideal, str) or hasattr(ideal, '__str__'):
            num = extract_ideal_number(str(ideal))
            if num is not None:
                return num
                
    raise ValueError("Could not parse witness")

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to "Prime ideals are irreducible"
    (where the hypothesis "P is a prime ideal" was dropped).
    """
    try:
        # Extract the generator of the ideal in Z
        n = get_preimage_generator(witness)
        # If we successfully extracted an ideal in Z or Z_n, the ring is commutative with identity.
        h1_ok = True
    except Exception:
        return [False, False]
        
    try:
        n = abs(n)
        # In Z, an ideal nZ is irreducible if and only if n is a prime power (or 0 or 1).
        # We want the negated conclusion (P is NOT irreducible), so we check if n has >= 2 distinct prime factors.
        if n == 0 or n == 1:
            neg_q_ok = False
        else:
            factors = factorint(n)
            if len(factors) > 1:
                neg_q_ok = True
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: P is not an irreducible ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1