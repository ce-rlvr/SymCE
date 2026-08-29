import math
from sympy import Integer
from sympy.abc import x, y, z

# Top-level setup for Ring Theory
# The witness is expected to be a list of integers representing ideals in Z,
# or a tuple (ring, ideals) where ideals is a list of integers.

def get_lcm(a, b):
    if a == 0 and b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    """
    # Extract ideals from witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[1], (list, tuple)):
            ideals = witness[1]
        else:
            ideals = witness
            
        # H1: R is a commutative ring
        # We verify this by checking if the witness represents ideals in Z (a commutative ring)
        h1 = isinstance(ideals, (list, tuple)) and all(isinstance(val, (int, Integer)) for val in ideals)
    except Exception:
        h1 = False
        ideals = []

    # H2: For all i != j, the radicals \sqrt{Q_i} and \sqrt{Q_j} are comaximal
    try:
        h2 = True
        if h1:
            for i in range(len(ideals)):
                for j in range(i + 1, len(ideals)):
                    # In Z, rad(a) and rad(b) are comaximal iff gcd(a, b) == 1
                    if math.gcd(int(ideals[i]), int(ideals[j])) != 1:
                        h2 = False
                        break
                if not h2:
                    break
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The intersection \bigcap_{i=1}^n Q_i is NOT equal to the product Q_1 Q_2 \cdots Q_n
    try:
        neg_q = False
        if h1 and len(ideals) > 0:
            intersection = int(ideals[0])
            product = int(ideals[0])
            for i in range(1, len(ideals)):
                val = int(ideals[i])
                intersection = get_lcm(intersection, val)
                product *= val
            # In Z, two principal ideals are equal iff their generators have the same absolute value
            neg_q = abs(intersection) != abs(product)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: For all i != j, the radicals of Q_i and Q_j are comaximal",
    "¬Q: The intersection of Q_i is not equal to their product"
]

N_HYP = 2
NEG_Q_INDEX = 2