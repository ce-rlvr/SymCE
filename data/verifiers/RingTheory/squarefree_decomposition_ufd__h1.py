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

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: a is a non-zero, non-unit element of R",
    "¬Q: a cannot be factored as a = b^2 c with c squarefree"
]

def conditions(witness):
    H1 = False
    neg_Q = False
    
    try:
        # Case 1: Custom object with methods
        if hasattr(witness, 'is_non_zero') and hasattr(witness, 'is_non_unit'):
            H1 = witness.is_non_zero() and witness.is_non_unit()
            if hasattr(witness, 'has_squarefree_decomp'):
                neg_Q = not witness.has_squarefree_decomp()
            elif hasattr(witness, 'can_factor_squarefree'):
                neg_Q = not witness.can_factor_squarefree()
            return [bool(H1), bool(neg_Q)]
            
        # Case 2: Tuple (R, a) or (a, R) where R is a finite ring (list/set/tuple) or a ring object
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], (list, tuple, set)):
                R, a = witness[0], witness[1]
            elif isinstance(witness[1], (list, tuple, set)):
                a, R = witness[0], witness[1]
            else:
                a, R = witness[0], witness[1]
                
            if isinstance(R, (list, tuple, set)):
                R = list(R)
                # Find zero element
                zero = None
                for x in R:
                    if all(x + y == y for y in R):
                        zero = x
                        break
                if zero is None: 
                    zero = R[0]
                
                # Find identity element
                one = None
                for x in R:
                    if all(x * y == y for y in R):
                        one = x
                        break
                if one is None: 
                    one = R[0]
                
                is_zero = (a == zero)
                
                is_unit = False
                for x in R:
                    if a * x == one or x * a == one:
                        is_unit = True
                        break
                
                H1 = (not is_zero) and (not is_unit)
                
                # Find all non-units
                non_units = []
                for x in R:
                    unit = False
                    for y in R:
                        if x * y == one or y * x == one:
                            unit = True
                            break
                    if not unit:
                        non_units.append(x)
                        
                squares_of_non_units = [x * x for x in non_units]
                
                def is_squarefree(c):
                    for s in squares_of_non_units:
                        for y in R:
                            if s * y == c or y * s == c:
                                return False
                    return True
                    
                can_factor = False
                for b in R:
                    b2 = b * b
                    for c in R:
                        if b2 * c == a:
                            if is_squarefree(c):
                                can_factor = True
                                break
                    if can_factor:
                        break
                        
                neg_Q = not can_factor
                return [bool(H1), bool(neg_Q)]
                
            # If R is an object with ring methods
            if hasattr(R, 'is_zero') and hasattr(R, 'is_unit'):
                H1 = (not R.is_zero(a)) and (not R.is_unit(a))
                if hasattr(R, 'has_squarefree_decomp'):
                    neg_Q = not R.has_squarefree_decomp(a)
                return [bool(H1), bool(neg_Q)]
                
        # Case 3: Integer (Z is a UFD, so neg_Q is False)
        if isinstance(witness, int):
            H1 = (witness != 0) and (abs(witness) != 1)
            neg_Q = False
            return [bool(H1), bool(neg_Q)]
            
        # Case 4: Sympy object (Sympy rings are Noetherian domains, so neg_Q is False)
        if hasattr(witness, 'is_zero'):
            H1 = not witness.is_zero
            if hasattr(witness, 'is_unit'):
                H1 = H1 and not witness.is_unit
            neg_Q = False
            return [bool(H1), bool(neg_Q)]
            
    except Exception:
        pass
        
    return [False, False]