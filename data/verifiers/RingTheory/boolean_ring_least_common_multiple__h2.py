import itertools

# Top-level setup for standard algebra objects
# (Not strictly needed for this specific ring theory verifier, but provided as requested)
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: The product ab is NOT a least common multiple of a and b in R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a ring R, or a tuple (R, a, b).
    R is expected to have `elements`, `add(x, y)`, and `mul(x, y)`.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, a, b = witness
            check_all = False
        else:
            R = witness
            check_all = True

        elements = list(R.elements)
        
        # H_1: R is a Boolean ring
        # Check if R is a ring and x^2 = x for all x
        h1_ok = False
        # Find additive identity (zero)
        zeros_list = [z for z in elements if all(R.add(z, x) == x and R.add(x, z) == x for x in elements)]
        if zeros_list:
            zero = zeros_list[0]
            h1_ok = True
            for x in elements:
                # Additive inverse exists
                if not any(R.add(x, y) == zero and R.add(y, x) == zero for y in elements):
                    h1_ok = False
                    break
                # Boolean ring property: x^2 = x
                if R.mul(x, x) != x:
                    h1_ok = False
                    break
                # Commutativity of addition
                for y in elements:
                    if R.add(x, y) != R.add(y, x):
                        h1_ok = False
                        break
                    # Associativity and distributivity
                    for z in elements:
                        if R.add(R.add(x, y), z) != R.add(x, R.add(y, z)):
                            h1_ok = False
                            break
                        if R.mul(R.mul(x, y), z) != R.mul(x, R.mul(y, z)):
                            h1_ok = False
                            break
                        if R.mul(x, R.add(y, z)) != R.add(R.mul(x, y), R.mul(x, z)):
                            h1_ok = False
                            break
                        if R.mul(R.add(x, y), z) != R.add(R.mul(x, z), R.mul(y, z)):
                            h1_ok = False
                            break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    if not h1_ok:
        return [False, False]

    # Helper to check divisibility in R: x divides y iff exists k in R such that y = x * k
    def divides(x, y):
        return any(R.mul(x, k) == y for k in elements)

    # Helper to check if m is a least common multiple of x and y in R
    def is_lcm(x, y, m):
        # m must be a common multiple
        if not (divides(x, m) and divides(y, m)):
            return False
        # m must divide any other common multiple c
        for c in elements:
            if divides(x, c) and divides(y, c):
                if not divides(m, c):
                    return False
        return True

    # ¬Q: The product ab is NOT a least common multiple of a and b in R
    neg_q_ok = False
    try:
        if check_all:
            # If only R is provided, we search for any pair (a, b) that falsifies the conclusion
            for x in elements:
                for y in elements:
                    prod = R.mul(x, y)
                    if not is_lcm(x, y, prod):
                        neg_q_ok = True
                        break
                if neg_q_ok:
                    break
        else:
            # If specific a and b are provided, check them
            prod = R.mul(a, b)
            neg_q_ok = not is_lcm(a, b, prod)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]