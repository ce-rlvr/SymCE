import sympy
from sympy import isprime
from sympy.abc import x, y, z
from sympy import Rational, Integer

# Top-level setup
# No specific named bindings are required for this domain,
# but we provide standard symbols and types.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a finite commutative ring with non-zero identity, and f: R -> S 
    is a ring homomorphism such that f(1_R) = 1_S, then f(R) is a finite field."
    
    The witness is expected to represent the ring Z/nZ (and optionally the image Z/mZ).
    It can be an integer `n` (implying R = S = Z/nZ and f is the identity),
    or a tuple `(n, m)` (implying R = Z/nZ, S = Z/mZ, and f is the natural projection).
    """
    try:
        # Parse the witness into n and m
        if hasattr(witness, 'is_Integer') and witness.is_Integer:
            n = int(witness)
            m = n
        elif isinstance(witness, (tuple, list)):
            if len(witness) >= 2:
                n, m = witness[0], witness[1]
            elif len(witness) == 1:
                n = witness[0]
                m = n
            else:
                return [False, False, False]
            n = int(n)
            m = int(m)
        elif isinstance(witness, (int, float)) and not isinstance(witness, bool):
            n = int(witness)
            m = n
        else:
            # Fallback: try to extract integers from string representation (e.g., "Z/4Z")
            s = str(witness)
            nums = []
            current = ""
            for char in s:
                if char.isdigit():
                    current += char
                elif current:
                    nums.append(int(current))
                    current = ""
            if current:
                nums.append(int(current))
            
            if len(nums) == 1:
                n = nums[0]
                m = n
            elif len(nums) >= 2:
                n = nums[0]
                m = nums[1]
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a finite commutative ring with non-zero identity
    # Z/nZ is a finite commutative ring. It has a non-zero identity iff n >= 2.
    try:
        h1 = (n >= 2)
    except Exception:
        h1 = False

    # H_2: f: R -> S is a ring homomorphism such that f(1_R) = 1_S
    # The natural projection Z/nZ -> Z/mZ is a well-defined ring homomorphism 
    # mapping 1 to 1 iff m divides n. We also require m >= 2 for a non-zero identity in S.
    try:
        h2 = (m >= 2) and (n % m == 0)
    except Exception:
        h2 = False

    # ¬Q: The image f(R) is NOT a finite field
    # The image is isomorphic to Z/mZ, which is a field iff m is prime.
    try:
        neg_q = not isprime(m)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a finite commutative ring with non-zero identity",
    "H_2: f: R -> S is a ring homomorphism such that f(1_R) = 1_S",
    "¬Q: The image f(R) is not a finite field"
]

N_HYP = 2
NEG_Q_INDEX = 2