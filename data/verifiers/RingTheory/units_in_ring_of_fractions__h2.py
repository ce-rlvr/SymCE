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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (R, S, s) where:
      - R is an integer n (representing the ring Z_n) or a custom ring object
      - S is a list/set of elements in R
      - s is an element in R
    """
    try:
        if not (isinstance(witness, tuple) and len(witness) == 3):
            return [False, False, False, False]
            
        R_obj, S, s = witness
        
        # Parse the ring R
        if isinstance(R_obj, int):
            if R_obj < 1:
                return [False, False, False, False]
            n = R_obj
            if n == 1:
                elements = [0]
                add = lambda x, y: 0
                mul = lambda x, y: 0
                zero = 0
                one = 0
            else:
                elements = list(range(n))
                add = lambda x, y: (x + y) % n
                mul = lambda x, y: (x * y) % n
                zero = 0
                one = 1
        else:
            elements = R_obj.elements
            add = R_obj.add
            mul = R_obj.mul
            zero = R_obj.zero
            one = R_obj.one
            
        S_list = list(S)
        if not all(x in elements for x in S_list):
            return [False, False, False, False]
            
        # H1: R is a commutative ring with identity
        h1 = True
        if one not in elements or zero not in elements:
            h1 = False
        else:
            for a in elements:
                if add(a, zero) != a or add(zero, a) != a: 
                    h1 = False
                    break
                if mul(a, one) != a or mul(one, a) != a: 
                    h1 = False
                    break
                
                has_neg = False
                for b in elements:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_neg = True
                        break
                if not has_neg: 
                    h1 = False
                    break
                
                for b in elements:
                    if add(a, b) not in elements: 
                        h1 = False; break
                    if mul(a, b) not in elements: 
                        h1 = False; break
                    if add(a, b) != add(b, a): 
                        h1 = False; break
                    if mul(a, b) != mul(b, a): 
                        h1 = False; break
                    
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): 
                            h1 = False; break
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): 
                            h1 = False; break
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): 
                            h1 = False; break
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): 
                            h1 = False; break
                    if not h1: break
                if not h1: break
                    
        # H2: 1 is in S
        h2 = one in S_list
        
        # H3: s is an element of S
        h3 = s in S_list
        
        # ¬Q: The fraction s/1 is NOT a unit in the ring of fractions S^(-1)R.
        # This occurs iff S^(-1)R fails to be a valid ring, which happens exactly
        # when S is not a multiplicatively closed subset.
        neg_q = False
        for x in S_list:
            for y in S_list:
                if mul(x, y) not in S_list:
                    neg_q = True
                    break
            if neg_q:
                break
                
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: 1 is in S",
    "H_3: s is an element of S",
    "¬Q: S^(-1)R is not a valid ring (S is not multiplicatively closed)"
]

N_HYP = 3
NEG_Q_INDEX = 3