import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    # 1. Try finite ring representation (dict or object with elements, mul, zero, a, b)
    try:
        if isinstance(witness, dict):
            elements = witness['elements']
            mul = witness['mul']
            zero = witness['zero']
            a = witness['a']
            b = witness['b']
        else:
            elements = witness.elements
            mul = witness.mul
            zero = witness.zero
            a = witness.a
            b = witness.b
            
        elements_set = set(elements)
        is_reduced = True
        
        # Check if the ring is reduced (no non-zero nilpotent elements).
        # For non-associative rings, we must check if any parenthesization of x^n is zero.
        for x in elements:
            if x == zero:
                continue
            
            generated = {x}
            new_elements = {x}
            nilpotent = False
            
            while new_elements:
                next_new = set()
                for elem1 in new_elements:
                    for elem2 in generated:
                        v1 = mul(elem1, elem2)
                        if v1 not in elements_set:
                            nilpotent = True
                            is_reduced = False
                            break
                        if v1 == zero:
                            nilpotent = True
                            break
                        if v1 not in generated:
                            next_new.add(v1)
                            
                        v2 = mul(elem2, elem1)
                        if v2 not in elements_set:
                            nilpotent = True
                            is_reduced = False
                            break
                        if v2 == zero:
                            nilpotent = True
                            break
                        if v2 not in generated:
                            next_new.add(v2)
                    if nilpotent:
                        break
                
                if not nilpotent:
                    for elem1 in new_elements:
                        for elem2 in new_elements:
                            v = mul(elem1, elem2)
                            if v not in elements_set:
                                nilpotent = True
                                is_reduced = False
                                break
                            if v == zero:
                                nilpotent = True
                                break
                            if v not in generated:
                                next_new.add(v)
                        if nilpotent:
                            break
                            
                if nilpotent:
                    is_reduced = False
                    break
                    
                generated.update(next_new)
                new_elements = next_new
                
            if not is_reduced:
                break
                
        ab = mul(a, b)
        ba = mul(b, a)
        h2 = bool(ab == zero)
        neg_q = bool(ba != zero)
        
        return [bool(is_reduced), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 2. Try tuple (ring, a, b) for sympy objects
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            ring, a, b = witness
            
            is_reduced = getattr(ring, 'is_domain', False)
            if not is_reduced and hasattr(ring, 'is_reduced'):
                is_reduced = ring.is_reduced
                
            ab = a * b
            ba = b * a
            
            if hasattr(ab, 'is_zero_matrix'):
                h2 = ab.is_zero_matrix
            elif hasattr(ab, 'is_zero'):
                h2 = ab.is_zero
            else:
                h2 = (ab == 0)
                
            if hasattr(ba, 'is_zero_matrix'):
                neg_q = not ba.is_zero_matrix
            elif hasattr(ba, 'is_zero'):
                neg_q = not ba.is_zero
            else:
                neg_q = (ba != 0)
                
            return [bool(is_reduced), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 3. Try custom object with a, b, zero
    try:
        a = witness.a
        b = witness.b
        zero = witness.zero
        
        if hasattr(witness, 'is_reduced'):
            is_reduced = witness.is_reduced() if callable(witness.is_reduced) else witness.is_reduced
        else:
            is_reduced = False
            
        ab = a * b
        ba = b * a
        
        if hasattr(ab, 'is_zero_matrix'):
            h2 = ab.is_zero_matrix
        elif hasattr(ab, 'is_zero'):
            h2 = ab.is_zero
        else:
            h2 = (ab == zero)
            
        if hasattr(ba, 'is_zero_matrix'):
            neg_q = not ba.is_zero_matrix
        elif hasattr(ba, 'is_zero'):
            neg_q = not ba.is_zero
        else:
            neg_q = (ba != zero)
        
        return [bool(is_reduced), bool(h2), bool(neg_q)]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a reduced ring (contains no non-zero nilpotent elements)",
    "H_2: ab = 0",
    "¬Q: ba != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2