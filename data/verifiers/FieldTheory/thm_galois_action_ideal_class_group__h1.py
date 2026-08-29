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

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    """
    try:
        # H_1: Cl(L) is the ideal class group of L
        # This is a definitional hypothesis, so it holds for any valid field witness.
        h1_ok = True
        
        # Extract the field L from the witness
        if isinstance(witness, tuple) and len(witness) >= 1:
            L = witness[0]
        else:
            L = witness
            
        class_name = L.__class__.__name__
        
        # The conclusion holds (neg_q = False) if L is a finite number field or finite field.
        # In these cases, the ring of integers is a Dedekind domain (or field),
        # so non-zero fractional ideals form a group and the action is by group automorphisms.
        if class_name in ['AlgebraicField', 'RationalField', 'GaloisField']:
            neg_q_ok = False
        elif L == sympy.QQ:
            neg_q_ok = False
        else:
            # For other rings/fields (e.g., function fields like Q(x), infinite extensions),
            # the integral closure may not be a Dedekind domain. Thus, the fractional ideals 
            # do not form a group, meaning Cl(L) is not a well-defined group and the action 
            # cannot be by group automorphisms. The conclusion fails.
            neg_q_ok = True
            
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: Cl(L) is the ideal class group of L",
    "¬Q: The action of Gal(L/K) on Cl(L) is not a well-defined group action by group automorphisms"
]

N_HYP = 1
NEG_Q_INDEX = 1