import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
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
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            if 'S' in witness and isinstance(witness['S'], dict):
                S_dict = witness['S']
                h1 = bool(S_dict.get('is_commutative', False)) and bool(S_dict.get('is_noetherian', False))
            else:
                h1 = bool(witness.get('S_is_commutative', witness.get('S_is_commutative_noetherian', False)))
                if 'S_is_noetherian' in witness:
                    h1 = h1 and bool(witness['S_is_noetherian'])
            
            if 'phi' in witness and isinstance(witness['phi'], dict):
                phi_dict = witness['phi']
                h2 = bool(phi_dict.get('is_flat', False))
                q = bool(phi_dict.get('satisfies_going_down', True))
            else:
                h2 = bool(witness.get('phi_is_flat', False))
                q = bool(witness.get('satisfies_going_down', witness.get('going_down', True)))
                
            neg_q = not q
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, S, phi = witness
        else:
            S = getattr(witness, 'S', witness)
            phi = getattr(witness, 'phi', witness)
            
        h1 = bool(getattr(S, 'is_commutative', False)) and bool(getattr(S, 'is_noetherian', False))
        h2 = bool(getattr(phi, 'is_flat', False))
        
        if hasattr(phi, 'satisfies_going_down'):
            q = bool(phi.satisfies_going_down)
        elif hasattr(witness, 'satisfies_going_down'):
            q = bool(witness.satisfies_going_down)
        else:
            q = True
            
        neg_q = not q
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a commutative Noetherian ring",
    "H_2: \\phi: R \\to S is a flat ring homomorphism",
    "¬Q: \\phi does not satisfy the Going-Down property for prime ideals"
]

N_HYP = 2
NEG_Q_INDEX = 2