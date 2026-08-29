import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools

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

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) in (4, 5):
            elements = witness[0]
            add = witness[1]
            mul = witness[2]
            zero = witness[3]
            size = len(elements)
            test_elems = list(elements)
            has_one = len(witness) == 5
            if has_one:
                one = witness[4]
        else:
            if hasattr(witness, 'size'):
                size = witness.size
            elif hasattr(witness, 'elements'):
                try:
                    size = len(witness.elements)
                except TypeError:
                    size = sympy.oo
            else:
                size = None
                
            if hasattr(witness, 'sample'):
                test_elems = list(witness.sample(15))
            elif hasattr(witness, 'elements'):
                test_elems = []
                for e in witness.elements:
                    test_elems.append(e)
                    if len(test_elems) >= 15:
                        break
            else:
                test_elems = []
                
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            has_one = hasattr(witness, 'one')
            if has_one:
                one = witness.one

        if test_elems and size is not None:
            is_ring = True
            for x in test_elems:
                if add(x, zero) != x: is_ring = False
                if add(zero, x) != x: is_ring = False
                if mul(x, x) != x: is_ring = False
                if add(x, x) != zero: is_ring = False
            
            if has_one:
                for x in test_elems:
                    if mul(x, one) != x: is_ring = False
                    if mul(one, x) != x: is_ring = False

            if is_ring:
                subset = list(test_elems)[:8]
                for x, y, z in itertools.product(subset, repeat=3):
                    if add(add(x, y), z) != add(x, add(y, z)): 
                        is_ring = False
                        break
                    if mul(mul(x, y), z) != mul(x, mul(y, z)): 
                        is_ring = False
                        break
                    if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): 
                        is_ring = False
                        break
                    if mul(add(x, y), z) != add(mul(x, z), mul(y, z)): 
                        is_ring = False
                        break
            
            h1 = is_ring
    except Exception:
        h1 = False

    try:
        if isinstance(witness, tuple) and len(witness) in (4, 5):
            size = len(witness[0])
        else:
            if hasattr(witness, 'size'):
                size = witness.size
            elif hasattr(witness, 'elements'):
                try:
                    size = len(witness.elements)
                except TypeError:
                    size = sympy.oo
            else:
                size = None
                
        if size is not None:
            if size == sympy.oo or size == math.inf or str(size).lower() in ['inf', 'infinity']:
                neg_q = True
            elif isinstance(size, int):
                if size < 1:
                    neg_q = True
                else:
                    if (size & (size - 1)) != 0:
                        neg_q = True
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: The number of elements in R is not 2^n for any non-negative integer n"
]

N_HYP = 1
NEG_Q_INDEX = 1