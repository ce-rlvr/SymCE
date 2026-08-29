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

# Top-level setup: named object bindings
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
    # Handle dictionary-based mock witnesses
    if isinstance(witness, dict):
        h1 = bool(witness.get('is_commutative', True))
        h2 = bool(witness.get('is_zariski', True))
        if 'V_IJ' in witness:
            neg_q = witness['V_IJ'] != (witness.get('V_I', set()) | witness.get('V_J', set()))
        else:
            neg_q = bool(witness.get('neg_Q', False))
        return [h1, h2, neg_q]
        
    h1, h2, neg_q = False, False, False
    
    # H_1: R is a commutative ring
    try:
        if hasattr(witness, 'is_commutative'):
            h1 = bool(witness.is_commutative)
        elif hasattr(witness, 'R') and hasattr(witness.R, 'is_commutative'):
            h1 = bool(witness.R.is_commutative)
        else:
            h1 = True  # Fallback if not explicitly provided
    except Exception:
        h1 = False

    # H_2: V(E) denotes the vanishing set of an ideal E in the Zariski topology on Spec(R)
    try:
        if hasattr(witness, 'is_zariski'):
            h2 = bool(witness.is_zariski)
        else:
            h2 = True  # Fallback if not explicitly provided
    except Exception:
        h2 = False

    # ¬Q: V(IJ) != V(I) \cup V(J)
    try:
        if hasattr(witness, 'V_IJ') and hasattr(witness, 'V_I') and hasattr(witness, 'V_J'):
            neg_q = witness.V_IJ != (witness.V_I | witness.V_J)
        elif hasattr(witness, 'V') and hasattr(witness, 'I') and hasattr(witness, 'J') and hasattr(witness, 'IJ'):
            neg_q = set(witness.V(witness.IJ)) != (set(witness.V(witness.I)) | set(witness.V(witness.J)))
        elif hasattr(witness, 'neg_Q'):
            neg_q = bool(witness.neg_Q)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: V(E) denotes the vanishing set of an ideal E in the Zariski topology on Spec(R)",
    "¬Q: V(IJ) != V(I) \\cup V(J)"
]

N_HYP = 2
NEG_Q_INDEX = 2