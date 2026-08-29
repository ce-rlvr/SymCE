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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_bool_attr(obj, *names):
    for name in names:
        try:
            if isinstance(obj, dict) and name in obj:
                val = obj[name]
            elif hasattr(obj, name):
                val = getattr(obj, name)
            else:
                continue
                
            if callable(val): 
                val = val()
                
            if isinstance(val, str):
                if val.lower() == 'false':
                    return False
                if val.lower() == 'true':
                    return True
            return bool(val)
        except Exception:
            continue
    return None

def conditions(witness) -> list[bool]:
    # H1: R is a commutative Noetherian ring
    try:
        if isinstance(witness, tuple) and len(witness) >= 1:
            R = witness[0]
        elif isinstance(witness, dict) and 'R' in witness:
            R = witness['R']
        elif hasattr(witness, 'R'):
            R = witness.R
        else:
            R = witness
            
        is_comm = get_bool_attr(R, 'is_commutative', 'commutative')
        is_noeth = get_bool_attr(R, 'is_noetherian', 'noetherian', 'is_Noetherian')
        
        if is_comm is None: 
            is_comm = False
        if is_noeth is None: 
            is_noeth = False
        
        h1 = is_comm and is_noeth
    except Exception:
        h1 = False

    # neg_Q: Ass(R/I^n) does NOT stabilize
    try:
        stabilizes = get_bool_attr(witness, 'ass_stabilizes', 'stabilizes', 'sequence_stabilizes', 'ass_sequence_stabilizes', 'is_ass_stabilized')
        if stabilizes is None:
            neg_q = False
        else:
            neg_q = not stabilizes
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: The sequence of sets of associated primes Ass(R/I^n) does not stabilize for all sufficiently large integers n"
]

N_HYP = 1
NEG_Q_INDEX = 1