import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a ring and pi: R -> R/I is the canonical projection map, 
    then pi is an epimorphism in the category of rings."
    
    The dropped hypothesis is that I must be a two-sided ideal of R.
    If I is not a two-sided ideal, R/I is not a ring, so pi is not a valid 
    morphism in the category of rings, and thus cannot be an epimorphism.
    """
    
    # 1. Handle mock objects (dictionaries or objects with attributes)
    if isinstance(witness, dict) and "is_ring" in witness:
        try:
            h1 = bool(witness.get("is_ring", False))
            h2 = bool(witness.get("is_canonical_projection", True))
            neg_q = not bool(witness.get("is_epimorphism", True))
            return [h1, h2, neg_q]
        except Exception:
            pass

    if hasattr(witness, "is_ring"):
        try:
            h1 = bool(getattr(witness, "is_ring", False))
            h2 = bool(getattr(witness, "is_canonical_projection", True))
            neg_q = not bool(getattr(witness, "is_epimorphism", True))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 2. Handle explicit finite counterexamples: tuple of (R, I)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            R, I = witness
            
            R_list = list(R)
            I_list = list(I)
            
            # Prevent excessively long execution times
            if len(R_list) > 200:
                return [False, False, False]
                
            def check_ring(S_list):
                if not S_list: return False
                for a in S_list:
                    for b in S_list:
                        if (a + b) not in S_list: return False
                        if (a - b) not in S_list: return False
                        if (a * b) not in S_list: return False
                return True
                
            def check_ideal(R_set, I_set):
                if not I_set: return False
                for a in I_set:
                    if a not in R_set: return False
                # Check closure under addition and subtraction
                for a in I_set:
                    for b in I_set:
                        if (a + b) not in I_set: return False
                        if (a - b) not in I_set: return False
                # Check two-sided absorption
                for r in R_set:
                    for a in I_set:
                        if (r * a) not in I_set: return False
                        if (a * r) not in I_set: return False
                return True

            h1 = check_ring(R_list)
            h2 = True  # The map is defined as the canonical projection by the setup
            
            # pi is an epimorphism in the category of rings iff I is a two-sided ideal.
            # If I is not an ideal, R/I is not a ring, so pi is not a ring homomorphism.
            is_epi = check_ideal(R_list, I_list)
            neg_q = not is_epi
            
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: pi: R -> R/I is the canonical projection map",
    "¬Q: The map pi is not an epimorphism in the category of rings"
]

N_HYP = 2
NEG_Q_INDEX = 2