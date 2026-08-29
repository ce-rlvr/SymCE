import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Given a witness group G, checks if it satisfies the remaining hypotheses
    and falsifies the conclusion.
    """
    # H_1: G is finitely generated
    try:
        # In SymPy, standard group representations (PermutationGroup, FpGroup) 
        # that have a 'generators' attribute are finitely generated.
        h1 = hasattr(witness, 'generators')
    except Exception:
        h1 = False

    # H_2: G is nilpotent
    try:
        nilp = getattr(witness, 'is_nilpotent')
        if callable(nilp):
            nilp = nilp()
        h2 = bool(nilp)
    except Exception:
        h2 = False

    # ¬Q: G is not a polycyclic group
    try:
        if hasattr(witness, 'is_polycyclic') and getattr(witness, 'is_polycyclic') is not None:
            poly = getattr(witness, 'is_polycyclic')
            if callable(poly):
                poly = poly()
            is_poly = bool(poly)
        else:
            # Fallback for finite groups (e.g., PermutationGroup)
            # A finite group is polycyclic if and only if it is solvable.
            solv = getattr(witness, 'is_solvable')
            if callable(solv):
                solv = solv()
            is_poly = bool(solv)
        neg_q = not is_poly
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is finitely generated",
    "H_2: G is nilpotent",
    "¬Q: G is not a polycyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2