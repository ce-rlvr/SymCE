import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.matrices import eye, zeros

# Top-level setup for standard groups
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

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (G, a, b)
    """
    try:
        G, a, b = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        # In SymPy, permutation groups have an 'is_group' property or we can check type
        h1_ok = hasattr(G, 'elements') and hasattr(G, 'is_group') and G.is_group
    except Exception:
        h1_ok = False

    # H_2: b is an element of G
    try:
        h2_ok = b in G.elements
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion must FAIL at the witness.
    # Conclusion: a and b are conjugate in G iff there exist x, y in G such that a = xy and b = yx
    try:
        # Check if a and b are conjugate in G
        # a and b are conjugate in G if there exists g in G such that a = g * b * g^-1
        are_conjugate = False
        for g in G.elements:
            if a == g * b * g**-1:
                are_conjugate = True
                break
        
        # Check if there exist x, y in G such that a = xy and b = yx
        exist_xy = False
        for x in G.elements:
            for y in G.elements:
                if a == x * y and b == y * x:
                    exist_xy = True
                    break
            if exist_xy:
                break
        
        # The conclusion is the iff statement: are_conjugate == exist_xy
        # We want the negation of the conclusion, so we want them to be DIFFERENT.
        neg_q_ok = (are_conjugate != exist_xy)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: b is an element of G",
    "¬Q: 'a and b are conjugate in G' is not equivalent to 'there exist x, y in G such that a = xy and b = yx'"
]

N_HYP = 2
NEG_Q_INDEX = 2