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

def _get_bool_attr(obj, *names, default=False):
    """Helper to safely extract boolean properties from a witness object."""
    for name in names:
        try:
            if hasattr(obj, name):
                val = getattr(obj, name)
                if callable(val):
                    return bool(val())
                else:
                    return bool(val)
        except Exception:
            continue
    return default

def conditions(witness) -> list[bool]:
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    try:
        # Handle dictionary-based witness
        if isinstance(witness, dict):
            h1_ok = bool(witness.get('is_commutative', False))
            h2_ok = bool(witness.get('is_Artinian', witness.get('is_artinian', False)))
            q = witness.get('localized_is_Artinian', witness.get('localized_is_artinian', True))
            neg_q_ok = not bool(q)
            return [h1_ok, h2_ok, neg_q_ok]
            
        # Handle tuple-based witness (R, S)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
            h1_ok = _get_bool_attr(R, 'is_commutative')
            h2_ok = _get_bool_attr(R, 'is_Artinian', 'is_artinian')
            
            q = True
            try:
                if hasattr(R, 'localization'):
                    loc = R.localization(S)
                    q = _get_bool_attr(loc, 'is_Artinian', 'is_artinian', default=True)
                elif hasattr(R, 'localize'):
                    loc = R.localize(S)
                    q = _get_bool_attr(loc, 'is_Artinian', 'is_artinian', default=True)
            except Exception:
                pass
            neg_q_ok = not q
            return [h1_ok, h2_ok, neg_q_ok]

        # Handle object-based witness
        h1_ok = _get_bool_attr(witness, 'is_commutative')
        h2_ok = _get_bool_attr(witness, 'is_Artinian', 'is_artinian')
        
        q = True
        if hasattr(witness, 'localized_is_Artinian') or hasattr(witness, 'localized_is_artinian'):
            q = _get_bool_attr(witness, 'localized_is_Artinian', 'localized_is_artinian', default=True)
        else:
            try:
                if hasattr(witness, 'localization'):
                    loc = witness.localization()
                    q = _get_bool_attr(loc, 'is_Artinian', 'is_artinian', default=True)
                elif hasattr(witness, 'localize'):
                    loc = witness.localize()
                    q = _get_bool_attr(loc, 'is_Artinian', 'is_artinian', default=True)
            except Exception:
                pass
        neg_q_ok = not q
        
    except Exception:
        pass
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is an Artinian ring",
    "¬Q: The localized ring S^{-1}R is not an Artinian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2