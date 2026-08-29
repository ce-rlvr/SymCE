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

from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    try:
        s = str(witness)
        
        # If the witness is a finite group, it is path-connected iff it has order 1
        if hasattr(witness, 'order'):
            try:
                if callable(witness.order):
                    val = witness.order()
                else:
                    val = witness.order
                neg_q = (val > 1)
                return [bool(neg_q)]
            except Exception:
                pass
                
        # A single matrix is a single point, hence path-connected
        if isinstance(witness, sympy.MatrixBase):
            neg_q = False
            
        elif isinstance(witness, (tuple, list)):
            if len(witness) > 0 and all(isinstance(x, sympy.MatrixBase) for x in witness):
                # A discrete set of multiple matrices is not path-connected
                neg_q = len(witness) > 1
            elif any(x == sympy.S.Reals or str(x) in ['R', 'Reals', 'RR', 'ℝ'] for x in witness):
                neg_q = True
            elif any(x == sympy.S.Complexes or str(x) in ['C', 'Complexes', 'CC', 'ℂ'] for x in witness):
                neg_q = False
            elif any(str(x) in ['H', 'Quaternions', 'HH', 'ℍ'] for x in witness):
                neg_q = False
            else:
                neg_q = True
                
        else:
            # If the witness is a field, the unitary group over R is O(n) which is disconnected.
            # Over C it is U(n) which is connected. Over H it is Sp(n) which is connected.
            if witness == sympy.S.Reals or s in ['R', 'Reals', 'RR', 'ℝ']:
                neg_q = True
            elif witness == sympy.S.Complexes or s in ['C', 'Complexes', 'CC', 'ℂ']:
                neg_q = False
            elif s in ['H', 'Quaternions', 'HH', 'ℍ']:
                neg_q = False
            # If the witness is a group name
            elif 'O(' in s or 'Orthogonal' in s:
                if 'SO(' in s or 'SpecialOrthogonal' in s:
                    neg_q = False
                else:
                    neg_q = True
            elif 'GL(' in s or 'GeneralLinear' in s:
                if 'R' in s or 'Reals' in s or 'ℝ' in s:
                    neg_q = True
                else:
                    neg_q = False
            elif 'U(' in s or 'Unitary' in s or 'SU(' in s:
                neg_q = False
            # If the witness is the dimension n
            elif isinstance(witness, int):
                neg_q = (witness < 0)
            elif hasattr(witness, 'is_integer') and witness.is_integer:
                neg_q = (int(witness) < 0)
            else:
                # Default to True for other fields (like Z, Q, finite fields) which yield disconnected groups
                neg_q = True
                
    except Exception:
        neg_q = False
        
    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: U(n) is not a path-connected topological space"
]

N_HYP = 0
NEG_Q_INDEX = 0