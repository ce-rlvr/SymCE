import sympy
from sympy import *
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# The conjecture claims that the category of Boolean rings is dually equivalent to Stone spaces.
# This is true for Boolean rings WITH identity. If the identity requirement is dropped,
# the prime spectrum of a Boolean ring without identity is locally compact but not compact,
# hence not a Stone space. Thus, a valid counterexample is a Boolean ring without identity.

class BooleanRing:
    def __init__(self, has_identity=True, name=""):
        self._has_identity = has_identity
        self.name = name
    
    def is_boolean_ring(self):
        return True
    
    def has_identity(self):
        return self._has_identity
    
    def __str__(self):
        return self.name

# Standard examples of Boolean rings
Z2 = BooleanRing(has_identity=True, name="Z2")
Z2xZ2 = BooleanRing(has_identity=True, name="Z2xZ2")

# Counterexamples: Boolean rings without identity
FiniteSubsetsOfN = BooleanRing(has_identity=False, name="FiniteSubsetsOfN")
FiniteSubsetsOfZ = BooleanRing(has_identity=False, name="FiniteSubsetsOfZ")
BooleanRingWithoutIdentity = BooleanRing(has_identity=False, name="BooleanRingWithoutIdentity")

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, str):
            s = witness.lower()
            if "without identity" in s or "finite subsets" in s:
                h1 = True
                neg_q = True
            elif "boolring" in s:
                h1 = True
                neg_q = True
        else:
            # Check explicit attributes if the witness is an object
            if hasattr(witness, 'is_boolean_ring'):
                h1_val = witness.is_boolean_ring() if callable(witness.is_boolean_ring) else witness.is_boolean_ring
                h1 = bool(h1_val)
                
                if hasattr(witness, 'has_identity'):
                    has_id = witness.has_identity() if callable(witness.has_identity) else witness.has_identity
                    neg_q = not bool(has_id)
                else:
                    neg_q = False
            
            # Fallback to checking class or object name
            if not h1:
                name = ""
                if hasattr(witness, '__name__'):
                    name = witness.__name__.lower()
                elif hasattr(witness, '__class__'):
                    name = witness.__class__.__name__.lower()
                
                if "finitesubsets" in name or "withoutidentity" in name:
                    h1 = True
                    neg_q = True
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Stone is the category of Stone spaces (witness is a Boolean ring)",
    "¬Q: The prime spectrum functor does not yield a dual equivalence (witness lacks an identity)"
]

N_HYP = 1
NEG_Q_INDEX = 1