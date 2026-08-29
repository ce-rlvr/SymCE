import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup

# Top-level setup: named object bindings that the witness expression may reference.
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: L/K is a finite Galois extension
    # In this context, we represent the Galois extension by its Galois group,
    # which must be a finite permutation group.
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # ¬Q: L is NOT the compositum of intermediate fields M_i where each M_i/K 
    # is a Galois extension of degree p_i^{e_i} for distinct primes p_i.
    # By Galois theory, this is equivalent to the Galois group NOT being nilpotent.
    try:
        if isinstance(witness, PermutationGroup):
            if callable(witness.is_nilpotent):
                is_nilp = witness.is_nilpotent()
            else:
                is_nilp = witness.is_nilpotent
            neg_q = not bool(is_nilp)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension (witness is a finite group)",
    "¬Q: L is not the compositum of intermediate fields M_i with Galois groups of distinct prime power degrees (Galois group is not nilpotent)"
]

N_HYP = 1
NEG_Q_INDEX = 1