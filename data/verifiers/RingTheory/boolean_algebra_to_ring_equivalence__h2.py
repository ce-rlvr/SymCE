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

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def is_boolean_algebra(B, vee, wedge, neg, zero, one):
    try:
        if zero not in B or one not in B: 
            return False
        for a in B:
            if neg(a) not in B: 
                return False
            for b in B:
                if vee(a, b) not in B: 
                    return False
                if wedge(a, b) not in B: 
                    return False
                
        for a in B:
            if vee(a, zero) != a: return False
            if vee(zero, a) != a: return False
            if wedge(a, one) != a: return False
            if wedge(one, a) != a: return False
            if vee(a, neg(a)) != one: return False
            if vee(neg(a), a) != one: return False
            if wedge(a, neg(a)) != zero: return False
            if wedge(neg(a), a) != zero: return False
            for b in B:
                if vee(a, b) != vee(b, a): return False
                if wedge(a, b) != wedge(b, a): return False
                if vee(a, wedge(a, b)) != a: return False
                if wedge(a, vee(a, b)) != a: return False
                for c in B:
                    if vee(a, vee(b, c)) != vee(vee(a, b), c): return False
                    if wedge(a, wedge(b, c)) != wedge(wedge(a, b), c): return False
                    if vee(a, wedge(b, c)) != wedge(vee(a, b), vee(a, c)): return False
                    if wedge(a, vee(b, c)) != vee(wedge(a, b), wedge(a, c)): return False
        return True
    except Exception:
        return False

def is_boolean_ring_with_identity(B, plus, dot, zero, one):
    try:
        if zero not in B or one not in B: 
            return False
        for a in B:
            for b in B:
                if plus(a, b) not in B: 
                    return False
                if dot(a, b) not in B: 
                    return False
                
        # Check (B, +, 0) is an abelian group
        for a in B:
            if plus(a, zero) != a or plus(zero, a) != a: 
                return False
            
            has_inverse = False
            for b in B:
                if plus(a, b) == zero and plus(b, a) == zero:
                    has_inverse = True
                    break
            if not has_inverse: 
                return False
            
            for b in B:
                if plus(a, b) != plus(b, a): 
                    return False
                for c in B:
                    if plus(a, plus(b, c)) != plus(plus(a, b), c): 
                        return False

        # Check (B, *, 1) is a monoid
        for a in B:
            if dot(a, one) != a or dot(one, a) != a: 
                return False
            for b in B:
                for c in B:
                    if dot(a, dot(b, c)) != dot(dot(a, b), c): 
                        return False

        # Check distributivity
        for a in B:
            for b in B:
                for c in B:
                    if dot(a, plus(b, c)) != plus(dot(a, b), dot(a, c)): 
                        return False
                    if dot(plus(a, b), c) != plus(dot(a, c), dot(b, c)): 
                        return False

        # Check Boolean ring property
        for a in B:
            if dot(a, a) != a: 
                return False

        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            B = list(witness['elements'])
            vee = witness['vee']
            wedge = witness['wedge']
            neg = witness['neg']
            zero = witness['zero']
            one = witness['one']
            plus = witness['plus']
            dot = witness.get('dot', wedge)
        else:
            B = list(witness.elements)
            vee = witness.vee
            wedge = witness.wedge
            neg = witness.neg
            zero = witness.zero
            one = witness.one
            plus = witness.plus
            dot = getattr(witness, 'dot', wedge)
    except Exception:
        return [False, False, False]
        
    h1 = is_boolean_algebra(B, vee, wedge, neg, zero, one)
    
    try:
        h2 = True
        for a in B:
            for b in B:
                if dot(a, b) != wedge(a, b):
                    h2 = False
    except Exception:
        h2 = False
        
    try:
        is_ring = is_boolean_ring_with_identity(B, plus, dot, zero, one)
        neg_q = not is_ring
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (B, vee, wedge, neg, 0, 1) is a Boolean algebra",
    "H_2: Multiplication is defined as a * b = a wedge b",
    "¬Q: (B, +, *, 0, 1) is not a Boolean ring with identity"
]

N_HYP = 2
NEG_Q_INDEX = 2