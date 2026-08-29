import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
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

# Free groups of various ranks
F1 = free_group('x')[0]
F2 = free_group('x, y')[0]
F3 = free_group('x, y, z')[0]

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, k) or a dict {'F': F, 'k': k} where:
      - F is a free group
      - k is an integer (the homology degree)
    """
    try:
        if isinstance(witness, dict):
            F = witness['F']
            k = witness['k']
        else:
            F, k = witness
    except Exception:
        return [False, False]

    # H_1: F is a free group
    try:
        h1 = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1 = False

    # ¬Q: The k-th group homology H_k(F, Z) is NOT the trivial group
    try:
        if not h1:
            neg_q = False
        elif not isinstance(k, (int, sympy.Integer)):
            neg_q = False
        else:
            k_val = int(k)
            try:
                n = F.rank
            except AttributeError:
                n = len(F.generators)
            
            # H_0(F, Z) = Z (not trivial)
            # H_1(F, Z) = Z^n (trivial iff n == 0)
            # H_k(F, Z) = 0 for k >= 2 (trivial)
            if k_val == 0:
                neg_q = True
            elif k_val == 1:
                neg_q = (n > 0)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: The k-th group homology H_k(F, Z) is not the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1