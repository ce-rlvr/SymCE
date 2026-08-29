import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: I is primary XOR Ass(R/I) consists of exactly one prime ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness can be provided as:
      - A 3-tuple: (is_proper: bool, is_primary: bool, ass_count: int)
      - A dictionary with keys 'is_proper', 'is_primary', and 'ass_count' (or 'associated_primes')
      - An object with attributes/methods `is_proper`, `is_primary`, and `ass_count` (or `associated_primes`)
    """
    try:
        # Tuple witness
        if isinstance(witness, tuple) and len(witness) == 3:
            is_proper, is_primary, ass_count = witness
            h1 = bool(is_proper)
            neg_q = bool(is_primary) != (ass_count == 1)
            return [h1, neg_q]
            
        # Dictionary witness
        if isinstance(witness, dict):
            is_proper = witness.get('is_proper', False)
            is_primary = witness.get('is_primary', False)
            if 'ass_count' in witness:
                ass_count = witness['ass_count']
            elif 'associated_primes' in witness:
                ap = witness['associated_primes']
                try:
                    ass_count = len(ap)
                except TypeError:
                    ass_count = len(list(ap))
            else:
                ass_count = -1
                
            h1 = bool(is_proper)
            neg_q = bool(is_primary) != (ass_count == 1) if ass_count != -1 else False
            return [h1, neg_q]
            
        # Object attributes witness
        is_proper = False
        if hasattr(witness, 'is_proper'):
            val = witness.is_proper
            is_proper = val() if callable(val) else val
        elif hasattr(witness, 'is_proper_ideal'):
            val = witness.is_proper_ideal
            is_proper = val() if callable(val) else val
            
        is_primary = False
        if hasattr(witness, 'is_primary'):
            val = witness.is_primary
            is_primary = val() if callable(val) else val
        elif hasattr(witness, 'is_primary_ideal'):
            val = witness.is_primary_ideal
            is_primary = val() if callable(val) else val
            
        ass_count = -1
        if hasattr(witness, 'ass_count'):
            val = witness.ass_count
            ass_count = val() if callable(val) else val
        elif hasattr(witness, 'associated_primes_count'):
            val = witness.associated_primes_count
            ass_count = val() if callable(val) else val
        elif hasattr(witness, 'associated_primes'):
            val = witness.associated_primes
            ap = val() if callable(val) else val
            try:
                ass_count = len(ap)
            except TypeError:
                ass_count = len(list(ap))
            
        h1 = bool(is_proper)
        neg_q = bool(is_primary) != (ass_count == 1) if ass_count != -1 else False
        return [h1, neg_q]
        
    except Exception:
        return [False, False]