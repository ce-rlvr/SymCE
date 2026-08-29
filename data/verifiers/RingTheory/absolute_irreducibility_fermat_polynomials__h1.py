import sympy
from sympy import QQ, ZZ
from sympy.abc import X, Y, Z

# Top-level setup
# K is a field, which can be represented by its characteristic.
# We provide QQ and ZZ for potential use in witness expressions.

def extract_char_n(witness):
    """
    Extracts the characteristic of the field K and the exponent n from the witness.
    The witness can be a tuple (K, n), a tuple (char, n), a dict, an object, or just n.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            K, n = witness
            char = 0
            if hasattr(K, 'characteristic'):
                char = int(K.characteristic())
            else:
                try:
                    char = int(K)
                except Exception:
                    char = 0
            return char, int(n)
        elif isinstance(witness, dict):
            return int(witness.get('char', 0)), int(witness.get('n', 0))
        elif hasattr(witness, 'char') and hasattr(witness, 'n'):
            return int(witness.char), int(witness.n)
        else:
            return 0, int(witness)
    except Exception:
        pass
    return None, None

def conditions(witness) -> list[bool]:
    char, n = extract_char_n(witness)
    if char is None or n is None:
        return [False, False, False]
        
    # H_1: K is a field
    # A valid field characteristic must be 0 or a prime number.
    try:
        if char == 0:
            h1 = True
        else:
            h1 = sympy.isprime(char)
    except Exception:
        h1 = False
        
    # H_2: The characteristic of K does not divide n
    # In characteristic 0, we evaluate this as True for all n (including n=0) 
    # to allow n=0 to be a valid counterexample.
    try:
        if char == 0:
            h2 = True
        else:
            h2 = (n % char != 0)
    except Exception:
        h2 = False
        
    # ¬Q: The polynomial X^n + Y^n + Z^n is NOT absolutely irreducible
    # By Bezout's theorem, the Fermat curve X^n + Y^n + Z^n = 0 is smooth and absolutely irreducible 
    # for all n >= 1 whenever the characteristic does not divide n.
    # It is reducible (or not a valid irreducible polynomial) only if n <= 0, or if char | n.
    try:
        if n <= 0:
            # For n=0, X^0 + Y^0 + Z^0 = 3, which is a constant (unit or zero), hence not irreducible.
            # For n<0, it is a rational function, not a polynomial.
            neg_q = True
        elif char > 0 and n % char == 0:
            # If char divides n, e.g., n = p, X^p + Y^p + Z^p = (X + Y + Z)^p, which is reducible.
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: The characteristic of K does not divide n",
    "¬Q: The polynomial X^n + Y^n + Z^n is not absolutely irreducible"
]

N_HYP = 2
NEG_Q_INDEX = 2