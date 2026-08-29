import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
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

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    # 1. Try to parse witness as a dictionary
    try:
        if isinstance(witness, dict):
            solvable = None
            galois = None
            for k, v in witness.items():
                k_lower = k.lower()
                if 'char' in k_lower and 'zero' in k_lower:
                    h1 = bool(v)
                elif 'split' in k_lower:
                    h2 = bool(v)
                elif 'radical' in k_lower:
                    solvable = bool(v)
                elif 'gal' in k_lower and 'solvable' in k_lower:
                    galois = bool(v)
            
            if solvable is None:
                for k, v in witness.items():
                    k_lower = k.lower()
                    if 'solvable' in k_lower and 'gal' not in k_lower:
                        solvable = bool(v)
                        
            if solvable is not None and galois is not None:
                neg_q = (solvable != galois)
            
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try to parse witness as an object with attributes
    try:
        solvable = None
        galois = None
        for k in dir(witness):
            if k.startswith('_'): continue
            try:
                v = getattr(witness, k)
                if callable(v): continue
                k_lower = k.lower()
                if 'char' in k_lower and 'zero' in k_lower:
                    h1 = bool(v)
                elif 'split' in k_lower:
                    h2 = bool(v)
                elif 'radical' in k_lower:
                    solvable = bool(v)
                elif 'gal' in k_lower and 'solvable' in k_lower:
                    galois = bool(v)
            except Exception:
                continue
                
        if solvable is None:
            for k in dir(witness):
                if k.startswith('_'): continue
                try:
                    v = getattr(witness, k)
                    if callable(v): continue
                    k_lower = k.lower()
                    if 'solvable' in k_lower and 'gal' not in k_lower:
                        solvable = bool(v)
                except Exception:
                    continue
                    
        if solvable is not None and galois is not None:
            neg_q = (solvable != galois)
            
        if any([h1, h2, solvable is not None, galois is not None]):
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try to parse witness as a tuple/list
    try:
        if isinstance(witness, (list, tuple)):
            # If exactly 3 booleans are provided: (h1, h2, neg_q)
            if len(witness) == 3 and all(isinstance(val, bool) for val in witness):
                return list(witness)
            # If 4 values are provided: (h1, h2, solvable, galois_solvable)
            if len(witness) >= 4:
                h1 = bool(witness[0])
                h2 = bool(witness[1])
                solvable = bool(witness[2])
                galois = bool(witness[3])
                neg_q = (solvable != galois)
                return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic zero",
    "H_2: K is the splitting field of f(x) over F",
    "¬Q: f(x) is solvable by radicals over F is not equivalent to Gal(K/F) being a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2