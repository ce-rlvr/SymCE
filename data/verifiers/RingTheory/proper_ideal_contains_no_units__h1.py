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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: I contains a unit of R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    H1 = False
    neg_Q = False
    
    # 1. Dictionary mock representation
    try:
        if isinstance(witness, dict):
            if 'is_proper_ideal' in witness:
                H1 = witness['is_proper_ideal']
            elif 'is_proper' in witness:
                H1 = witness['is_proper']
                
            if 'contains_unit' in witness:
                neg_Q = witness['contains_unit']
            elif 'contains_units' in witness:
                neg_Q = witness['contains_units']
                
            if H1 or neg_Q:
                return [bool(H1), bool(neg_Q)]
    except Exception:
        pass

    # 2. Finite ring represented as lists/sets of elements
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (list, set, tuple)):
            R, I = witness
            R = list(R)
            I = list(I)
            
            # Find multiplicative identity
            e = None
            for x in R:
                if all(x * y == y and y * x == y for y in R):
                    e = x
                    break
                    
            if e is not None:
                # Check proper ideal
                is_subset = all(x in R for x in I)
                is_proper = is_subset and len(I) < len(R)
                
                is_ideal = True
                for x in I:
                    for r in R:
                        if (r * x) not in I or (x * r) not in I:
                            is_ideal = False
                            break
                            
                # Check additive subgroup
                zero = None
                for z in R:
                    if all(z + x == x and x + z == x for x in R):
                        zero = z
                        break
                if zero not in I:
                    is_ideal = False
                for x in I:
                    for y in I:
                        if (x + y) not in I:
                            is_ideal = False
                            break
                            
                if is_proper and is_ideal:
                    H1 = True
                    
                # Check units
                for x in I:
                    is_u = False
                    for y in R:
                        if x * y == e and y * x == e:
                            is_u = True
                            break
                    if is_u:
                        neg_Q = True
                        break
            if H1 or neg_Q:
                return [bool(H1), bool(neg_Q)]
    except Exception:
        pass

    # 3. Object with attributes (e.g., sympy Ideal or custom class)
    try:
        obj = witness
        R_obj = None
        if isinstance(witness, tuple) and len(witness) == 2:
            R_obj, obj = witness
        else:
            R_obj = getattr(obj, 'ring', None)
            
        # Check H1: proper ideal
        if hasattr(obj, 'is_proper_ideal'):
            val = obj.is_proper_ideal
            H1 = val() if callable(val) else val
        elif hasattr(obj, 'is_proper'):
            val = obj.is_proper
            H1 = val() if callable(val) else val
        elif hasattr(obj, 'is_whole_ring'):
            val = obj.is_whole_ring
            H1 = not (val() if callable(val) else val)
            
        # Check neg_Q: contains a unit
        if hasattr(obj, 'contains_units'):
            val = obj.contains_units
            neg_Q = val() if callable(val) else val
        elif hasattr(obj, 'contains_unit'):
            val = obj.contains_unit
            neg_Q = val() if callable(val) else val
        else:
            if R_obj is not None:
                # If the ideal contains the identity, it contains a unit
                if hasattr(R_obj, 'one') and hasattr(obj, 'contains'):
                    if obj.contains(R_obj.one):
                        neg_Q = True
                # Check if any generator is a unit
                if hasattr(obj, 'gens'):
                    for g in obj.gens:
                        if hasattr(R_obj, 'is_unit') and R_obj.is_unit(g):
                            neg_Q = True
                        elif hasattr(g, 'is_unit') and g.is_unit:
                            neg_Q = True
    except Exception:
        pass

    return [bool(H1), bool(neg_Q)]