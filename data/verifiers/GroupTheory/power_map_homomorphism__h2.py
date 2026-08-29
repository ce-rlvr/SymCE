import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (G, n) where G is a group and n is an integer exponent.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            n = 2
    except Exception:
        return [False, False, False]

    # H_1: G is an abelian group
    try:
        if hasattr(G, 'is_abelian'):
            h1_ok = bool(G.is_abelian)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: f is a map from G to G defined by f(x) = x^n for all x in G
    try:
        # We verify that n is an integer, which makes the power map well-defined on G
        h2_ok = isinstance(n, (int, sympy.Integer))
    except Exception:
        h2_ok = False

    # ¬Q: f is not a group homomorphism
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        is_hom = True
        for x in elements:
            for y in elements:
                xy = x * y
                f_xy = xy ** n
                f_x = x ** n
                f_y = y ** n
                if f_xy != f_x * f_y:
                    is_hom = False
                    break
            if not is_hom:
                break
        neg_q_ok = not is_hom
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: f is a map from G to G defined by f(x) = x^n for all x in G",
    "¬Q: f is not a group homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2