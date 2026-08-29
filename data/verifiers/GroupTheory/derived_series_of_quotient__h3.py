import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, N, n) or a dict with these keys.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            n = witness.get('n')
        else:
            G, N, n = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: N is a normal subgroup of G
    try:
        h2_ok = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2_ok = False

    # ¬Q: The n-th derived subgroup of G/N is NOT equal to the subgroup (G^(n)N)/N.
    # Mathematically, the n-th derived subgroup of G/N is always equal to (G^(n)N)/N 
    # for any non-negative integer n. The conjecture fails when n is negative or not an integer,
    # because the n-th derived subgroup is undefined in those cases.
    try:
        if isinstance(n, (int, sympy.Integer)):
            is_valid_n = (n >= 0)
        elif isinstance(n, float) and n.is_integer():
            is_valid_n = (n >= 0)
        else:
            is_valid_n = False
            
        neg_q_ok = not is_valid_n
    except Exception:
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The n-th derived subgroup of G/N is not equal to the subgroup (G^(n)N)/N"
]

N_HYP = 2
NEG_Q_INDEX = 2