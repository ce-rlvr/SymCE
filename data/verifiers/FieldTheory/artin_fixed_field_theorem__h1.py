import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since the domain is abstract field theory and SymPy cannot natively compute
    Galois groups of arbitrary abstract extensions, the witness is expected to be
    a dictionary or an object with boolean attributes representing the mathematical properties.
    """
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("G_is_finite_group_of_automorphisms_of_K", witness.get("H1", False)))
            h2 = bool(witness.get("F_is_fixed_field_of_K_under_G", witness.get("H2", False)))
            q1 = bool(witness.get("K_over_F_is_finite_Galois", witness.get("Q1", False)))
            q2 = bool(witness.get("Gal_K_F_equals_G", witness.get("Q2", False)))
        else:
            h1 = bool(getattr(witness, "G_is_finite_group_of_automorphisms_of_K", getattr(witness, "H1", False)))
            h2 = bool(getattr(witness, "F_is_fixed_field_of_K_under_G", getattr(witness, "H2", False)))
            q1 = bool(getattr(witness, "K_over_F_is_finite_Galois", getattr(witness, "Q1", False)))
            q2 = bool(getattr(witness, "Gal_K_F_equals_G", getattr(witness, "Q2", False)))
            
        # The conclusion is that K/F is a finite Galois extension AND Gal(K/F) = G.
        # The negated conclusion is True if either of these fails.
        neg_q = not (q1 and q2)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a finite group of automorphisms of K",
    "H_2: F is the fixed field of K under the action of G",
    "¬Q: K/F is not a finite Galois extension or Gal(K/F) != G"
]

N_HYP = 2
NEG_Q_INDEX = 2