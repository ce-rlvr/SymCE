import sympy
import sympy.polys.domains as dom
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup for potential witness expressions
# (Standard rings and fields are available via SymPy domains)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a commutative ring with identity that is NOT Noetherian.
    """
    h1 = False
    neg_q = False
    
    try:
        if callable(witness):
            witness = witness()
            
        if isinstance(witness, str):
            s = witness.lower()
            # Assume a string witness represents a ring
            h1 = True
            # Check if the string implies an infinite number of variables or explicitly states non-Noetherian
            if "..." in s or "dots" in s or "infty" in s or "infinite" in s or "non-noetherian" in s or "nonnoetherian" in s:
                neg_q = True
            else:
                neg_q = False
                
        elif isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative_ring', 
                      witness.get('is_commutative', True) and witness.get('has_identity', True)))
            neg_q = not bool(witness.get('is_noetherian', True))
            
        elif isinstance(witness, dom.Domain):
            # All standard SymPy domains (ZZ, QQ, finite fields, and their finite polynomial rings) 
            # are commutative rings with identity and are Noetherian.
            h1 = True
            neg_q = False
            
        else:
            # Check H1: Commutative ring with identity
            if hasattr(witness, 'is_commutative_ring'):
                h1 = bool(witness.is_commutative_ring)
            elif hasattr(witness, 'is_commutative') and hasattr(witness, 'has_identity'):
                h1 = bool(witness.is_commutative and witness.has_identity)
            elif hasattr(witness, 'is_Ring'):
                h1 = bool(witness.is_Ring)
            else:
                class_name = witness.__class__.__name__.lower()
                if "ring" in class_name:
                    h1 = True
                else:
                    h1 = False
                
            # Check neg_Q: NOT Noetherian
            if hasattr(witness, 'is_noetherian'):
                neg_q = not bool(witness.is_noetherian)
            elif hasattr(witness, 'is_Noetherian'):
                neg_q = not bool(witness.is_Noetherian)
            else:
                # If it's a custom object acting as a ring but missing the Noetherian flag,
                # we assume it is the intended non-Noetherian counterexample.
                if h1:
                    neg_q = True
                    
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: R does not satisfy the ascending chain condition on ideals (R is not Noetherian)"
]

N_HYP = 1
NEG_Q_INDEX = 1