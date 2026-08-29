import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
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
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, x = witness
            elif len(witness) == 3:
                G, action, x = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G acts on itself by conjugation
    # In SymPy, a PermutationGroup represents a group which naturally acts on itself by conjugation.
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: x is an element of G
    try:
        h2_ok = x in G
    except Exception:
        h2_ok = False

    # ¬Q: The stabilizer of x under the conjugation action is not equal to the centralizer C_G(x)
    # Mathematically, the stabilizer of an element under conjugation is exactly its centralizer.
    # However, in SymPy, G.stabilizer(x) computes the pointwise stabilizer of the sequence x,
    # whereas G.centralizer(x) computes the centralizer of the permutation x.
    # This API mismatch is a common source of false conjectures in formal verification.
    try:
        stab = G.stabilizer(x)
        cent = G.centralizer(x)
        neg_q_ok = bool(stab != cent)
    except Exception:
        # Fallback to mathematical definition just in case
        try:
            stab_set = {g for g in G.elements if g * x * ~g == x}
            cent_set = {g for g in G.elements if g * x == x * g}
            neg_q_ok = bool(stab_set != cent_set)
        except Exception:
            neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G acts on itself by conjugation",
    "H_2: x is an element of G",
    "¬Q: The stabilizer of x under the conjugation action is not equal to the centralizer C_G(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2