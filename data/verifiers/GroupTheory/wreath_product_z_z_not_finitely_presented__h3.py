import sympy
from sympy.combinatorics import free_group, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

# The infinite cyclic group Z
Z, _x = free_group("x")

def is_Z(group):
    """Check if the group is isomorphic to the infinite cyclic group Z."""
    if type(group).__name__ == 'FreeGroup' and len(group.generators) == 1:
        return True
    if type(group).__name__ == 'FpGroup':
        if len(group.generators) == 1 and len(group.relators) == 0:
            return True
    return False

def is_finitely_generated(G):
    """Check if G is finitely generated."""
    return type(G).__name__ in ('FreeGroup', 'FpGroup') or isinstance(G, PermutationGroup)

def is_finitely_presented(G):
    """Check if G is finitely presented."""
    return type(G).__name__ in ('FreeGroup', 'FpGroup') or isinstance(G, PermutationGroup)

def conditions(witness) -> list[bool]:
    # Extract A, B, G from the witness
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            A, B, G = witness
        elif isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            G = witness.get('G')
        else:
            A, B, G = witness
    except Exception:
        return [False, False, False]

    # H_1: A is the infinite cyclic group Z
    try:
        h1_ok = is_Z(A)
    except Exception:
        h1_ok = False

    # H_2: B is the infinite cyclic group Z
    try:
        h2_ok = is_Z(B)
    except Exception:
        h2_ok = False

    # ¬Q: G is NOT (finitely generated but not finitely presented)
    # i.e., G is not finitely generated OR G is finitely presented
    try:
        fin_gen = is_finitely_generated(G)
        fin_pres = is_finitely_presented(G)
        q_ok = fin_gen and (not fin_pres)
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is the infinite cyclic group Z",
    "H_2: B is the infinite cyclic group Z",
    "¬Q: G is not finitely generated or G is finitely presented"
]

N_HYP = 2
NEG_Q_INDEX = 2