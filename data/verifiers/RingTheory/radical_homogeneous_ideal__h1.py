import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

# Top-level setup
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
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The theorem "The radical of a homogeneous ideal is a homogeneous ideal" is true for 
    commutative rings graded by torsion-free groups (like N or Z), but fails for rings 
    graded by groups with torsion (like Z/2Z) or non-commutative rings.
    Since SymPy does not natively support such gradings, the witness is expected to be 
    a custom object, dictionary, or tuple providing the truth values.
    """
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_homogeneous_ideal', witness.get('is_homogeneous', witness.get('h1', False))))
            
            if 'radical_not_homogeneous' in witness:
                neg_q = bool(witness['radical_not_homogeneous'])
            elif 'radical_is_homogeneous' in witness:
                neg_q = not bool(witness['radical_is_homogeneous'])
            else:
                neg_q = bool(witness.get('neg_q', False))
                
        elif isinstance(witness, (list, tuple)) and len(witness) >= 2 and all(isinstance(x, bool) for x in witness[:2]):
            h1 = bool(witness[0])
            neg_q = bool(witness[1])
            
        else:
            if hasattr(witness, 'is_homogeneous_ideal'):
                val = witness.is_homogeneous_ideal
                h1 = bool(val() if callable(val) else val)
            elif hasattr(witness, 'is_homogeneous'):
                val = witness.is_homogeneous
                h1 = bool(val() if callable(val) else val)
            elif hasattr(witness, 'h1'):
                val = witness.h1
                h1 = bool(val() if callable(val) else val)
                
            if hasattr(witness, 'radical_not_homogeneous'):
                val = witness.radical_not_homogeneous
                neg_q = bool(val() if callable(val) else val)
            elif hasattr(witness, 'radical_is_homogeneous'):
                val = witness.radical_is_homogeneous
                neg_q = not bool(val() if callable(val) else val)
            elif hasattr(witness, 'neg_q'):
                val = witness.neg_q
                neg_q = bool(val() if callable(val) else val)
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is a homogeneous ideal of R",
    "¬Q: The radical of I is not a homogeneous ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1