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

# Top-level setup
# SymPy does not have a comprehensive non-commutative ring theory module.
# The witness is expected to be a mock object or dictionary, or a tuple (R, I) of such objects,
# that explicitly provides the properties needed to evaluate the conjecture.
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
    The witness can be a tuple (R, I) or a single object/dict containing the properties.
    """
    h1 = False
    h2 = False
    neg_q = False

    # Check if witness is a tuple/list of (R, I)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            R, I = witness
            
            if isinstance(R, dict):
                h1 = bool(R.get('is_Noetherian_ring', R.get('is_noetherian', False)))
            else:
                h1 = bool(getattr(R, 'is_Noetherian_ring', getattr(R, 'is_noetherian', False)))
                
            if isinstance(I, dict):
                h2 = bool(I.get('is_ideal', False))
                q = bool(I.get('radical_power_contained', True))
            else:
                h2 = bool(getattr(I, 'is_ideal', False))
                q = bool(getattr(I, 'radical_power_contained', True))
                
            neg_q = not q
            return [h1, h2, neg_q]
    except Exception:
        pass

    # Fallback: witness is a single object or dictionary representing the counterexample
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_Noetherian_ring', witness.get('is_noetherian', False)))
            h2 = bool(witness.get('is_ideal', False))
            q = bool(witness.get('radical_power_contained', True))
        else:
            h1 = bool(getattr(witness, 'is_Noetherian_ring', getattr(witness, 'is_noetherian', False)))
            h2 = bool(getattr(witness, 'is_ideal', False))
            q = bool(getattr(witness, 'radical_power_contained', True))
            
        neg_q = not q
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: I is an ideal of R",
    "¬Q: There does not exist a positive integer k such that (\\sqrt{I})^k \\subseteq I"
]

N_HYP = 2
NEG_Q_INDEX = 2