import itertools
import math
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *

# Top-level setup: named object bindings
# We provide standard finite Boolean rings represented as sets of integers,
# where addition is bitwise XOR and multiplication is bitwise AND.
Z2 = {0, 1}
Z2xZ2 = {0, 1, 2, 3}
Z2xZ2xZ2 = {0, 1, 2, 3, 4, 5, 6, 7}

class CustomRing:
    """
    A helper class for users to define their own finite rings.
    """
    def __init__(self, elements, add, mul, zero=None):
        self.elements = elements
        self.add = add
        self.mul = mul
        self.zero = zero

def conditions(witness) -> list[bool]:
    try:
        elements = []
        
        # Extract elements and operations from the witness
        if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
            for i, e in enumerate(witness.elements):
                if i >= 64: return [False, False]  # Limit size for performance
                elements.append(e)
            add = witness.add
            mul = witness.mul
            zero = witness.zero if hasattr(witness, 'zero') else None
            
            # Auto-detect zero if not provided
            if zero is None:
                for e in elements:
                    if all(add(e, x) == x for x in elements):
                        zero = e
                        break
                        
        elif isinstance(witness, (list, set, tuple)) and all(isinstance(x, int) for x in witness):
            for i, e in enumerate(witness):
                if i >= 64: return [False, False]
                elements.append(e)
            # Default to bitwise operations for integer sets (isomorphic to power set rings)
            add = lambda a, b: a ^ b
            mul = lambda a, b: a & b
            zero = 0
        else:
            return [False, False]
            
        if not elements:
            return [False, False]
            
        if zero not in elements:
            return [False, False]
            
        # H_1: Check if it is a Boolean ring
        is_boolean = True
        for a in elements:
            # Identity
            if add(a, zero) != a: 
                is_boolean = False
                break
            if add(zero, a) != a: 
                is_boolean = False
                break
                
            # Boolean property (x^2 = x)
            if mul(a, a) != a: 
                is_boolean = False
                break
            
            # Additive inverse
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: 
                is_boolean = False
                break
            
            for b in elements:
                # Closure
                if add(a, b) not in elements: 
                    is_boolean = False
                    break
                if mul(a, b) not in elements: 
                    is_boolean = False
                    break
                    
                # Commutativity of addition
                if add(a, b) != add(b, a): 
                    is_boolean = False
                    break
                
                for c in elements:
                    # Associativity
                    if add(a, add(b, c)) != add(add(a, b), c): 
                        is_boolean = False
                        break
                    if mul(a, mul(b, c)) != mul(mul(a, b), c): 
                        is_boolean = False
                        break
                        
                    # Distributivity
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): 
                        is_boolean = False
                        break
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): 
                        is_boolean = False
                        break
                        
                if not is_boolean: break
            if not is_boolean: break
            
        h1_ok = is_boolean
        
        # ¬Q: R is not isomorphic to Z/2Z
        # Any Boolean ring of size 2 is isomorphic to Z/2Z.
        # Therefore, it is NOT isomorphic to Z/2Z if and only if its size is not 2.
        neg_q_ok = len(elements) != 2
        
        return [h1_ok, neg_q_ok]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: R is not isomorphic to the field with two elements ℤ/2ℤ"
]

N_HYP = 1
NEG_Q_INDEX = 1