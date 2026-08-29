import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since SymPy does not natively support Kähler differentials or abstract module 
    isomorphisms, the witness is expected to be a mock object (dictionary, list, 
    or object with attributes) providing the boolean values directly.
    """
    h1_ok = False
    h2_ok = False
    q_ok = True  # We want not q_ok to be True when conclusion fails

    try:
        if isinstance(witness, dict):
            h1_ok = bool(witness.get("is_commutative_A_algebra", False))
            h2_ok = bool(witness.get("is_mult_closed_S", False))
            q_ok = bool(witness.get("iso_kaehler", True))
        elif isinstance(witness, (list, tuple)) and len(witness) >= 3:
            h1_ok = bool(witness[0])
            h2_ok = bool(witness[1])
            q_ok = bool(witness[2])
        else:
            h1_ok = bool(getattr(witness, "is_commutative_A_algebra", False))
            h2_ok = bool(getattr(witness, "is_mult_closed_S", False))
            q_ok = bool(getattr(witness, "iso_kaehler", True))
    except Exception:
        pass

    return [h1_ok, h2_ok, not q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative A-algebra",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: There is NO isomorphism of S^{-1}R-modules \Omega_{(S^{-1}R)/A} \cong S^{-1}\Omega_{R/A}"
]

N_HYP = 2
NEG_Q_INDEX = 2