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
    Evaluates the hypotheses and the negated conclusion for the conjecture:
    "Localization of a flat module is flat"
    
    Since SymPy does not have a comprehensive module theory library to natively 
    compute flatness or localizations of arbitrary modules, this verifier 
    checks for explicit properties provided on the witness object.
    """
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    try:
        if isinstance(witness, dict):
            h1_ok = bool(witness.get('is_flat_R_module', witness.get('is_flat', False)))
            h2_ok = bool(witness.get('is_multiplicatively_closed', False))
            # neg_q is True when the conclusion FAILS (i.e., localized module is NOT flat)
            neg_q_ok = not bool(witness.get('is_localized_flat', True))
            
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, M, S = witness
            h1_ok = bool(getattr(M, 'is_flat_R_module', getattr(M, 'is_flat', False)))
            h2_ok = bool(getattr(S, 'is_multiplicatively_closed', False))
            neg_q_ok = not bool(getattr(M, 'is_localized_flat', True))
            
        else:
            h1_ok = bool(getattr(witness, 'is_flat_R_module', getattr(witness, 'is_flat', False)))
            h2_ok = bool(getattr(witness, 'is_multiplicatively_closed', False))
            neg_q_ok = not bool(getattr(witness, 'is_localized_flat', True))
            
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: M is a flat R-module",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}M is not a flat module over S^{-1}R"
]

N_HYP = 2
NEG_Q_INDEX = 2