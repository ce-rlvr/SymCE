import math

# Top-level setup
# No special named objects needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    
    Remaining hypotheses:
      - Let (a, b, c) be a primitive Pythagorean triple with hypotenuse c
    
    Conclusion (must FAIL at the witness):
      The area A and the hypotenuse c are coprime integers.
    """
    try:
        # Witness should be a tuple or list of three integers (a, b, c)
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False]
        
        a, b, c = witness
        
        # Check if they are integers
        if not (isinstance(a, int) and isinstance(b, int) and isinstance(c, int)):
            return [False, False]
            
        # H1: (a, b, c) is a primitive Pythagorean triple with hypotenuse c
        # 1. a^2 + b^2 = c^2
        is_pythagorean = (a**2 + b**2 == c**2)
        # 2. Primitive: gcd(a, b, c) == 1
        is_primitive = (math.gcd(math.gcd(a, b), c) == 1)
        # 3. Usually, a Pythagorean triple consists of positive integers, but we allow non-zero integers
        # as long as they form a valid triangle.
        is_valid_triangle = (a != 0 and b != 0 and c != 0)
        
        h1_ok = bool(is_pythagorean and is_primitive and is_valid_triangle)
    except Exception:
        h1_ok = False

    try:
        # Conclusion: The area A and the hypotenuse c are coprime integers.
        # Area A = |a * b| / 2
        # For a primitive Pythagorean triple, exactly one of a or b is even, so a*b is divisible by 2.
        # Thus A is an integer.
        area = abs(a * b) // 2
        
        # Check if A and c are coprime
        are_coprime = (math.gcd(area, abs(c)) == 1)
        
        # The conclusion FAILS if they are NOT coprime
        neg_q_ok = not are_coprime
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (a, b, c) is a primitive Pythagorean triple with hypotenuse c",
    "¬Q: The area A and the hypotenuse c are NOT coprime integers"
]

N_HYP = 1
NEG_Q_INDEX = 1