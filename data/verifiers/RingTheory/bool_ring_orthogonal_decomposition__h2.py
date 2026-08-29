import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # Extract witness components
        elements, add_op, mul_op, zero, x, y = None, None, None, None, None, None
        
        if isinstance(witness, dict):
            if 'R' in witness:
                R = witness['R']
                x = witness.get('x')
                y = witness.get('y')
                if isinstance(R, dict):
                    elements = R.get('elements')
                    add_op = R.get('add')
                    mul_op = R.get('mul')
                    zero = R.get('zero')
                else:
                    elements = getattr(R, 'elements', None)
                    add_op = getattr(R, 'add', None)
                    mul_op = getattr(R, 'mul', None)
                    zero = getattr(R, 'zero', None)
            else:
                elements = witness.get('elements')
                add_op = witness.get('add')
                mul_op = witness.get('mul')
                zero = witness.get('zero')
                x = witness.get('x')
                y = witness.get('y')
        elif isinstance(witness, tuple):
            if len(witness) == 6:
                elements, add_op, mul_op, zero, x, y = witness
            elif len(witness) == 3:
                R, x, y = witness
                if isinstance(R, dict):
                    elements = R.get('elements')
                    add_op = R.get('add')
                    mul_op = R.get('mul')
                    zero = R.get('zero')
                else:
                    elements = getattr(R, 'elements', None)
                    add_op = getattr(R, 'add', None)
                    mul_op = getattr(R, 'mul', None)
                    zero = getattr(R, 'zero', None)
        else:
            if hasattr(witness, 'R'):
                R = witness.R
                x = getattr(witness, 'x', None)
                y = getattr(witness, 'y', None)
                if isinstance(R, dict):
                    elements = R.get('elements')
                    add_op = R.get('add')
                    mul_op = R.get('mul')
                    zero = R.get('zero')
                else:
                    elements = getattr(R, 'elements', None)
                    add_op = getattr(R, 'add', None)
                    mul_op = getattr(R, 'mul', None)
                    zero = getattr(R, 'zero', None)
            else:
                elements = getattr(witness, 'elements', None)
                add_op = getattr(witness, 'add', None)
                mul_op = getattr(witness, 'mul', None)
                zero = getattr(witness, 'zero', None)
                x = getattr(witness, 'x', None)
                y = getattr(witness, 'y', None)
                
        if elements is None:
            return [False, False]
            
        elements = list(elements)
        
        def make_callable(op):
            if callable(op): return op
            if isinstance(op, (list, tuple)): return lambda a, b: op[a][b]
            if isinstance(op, dict): return lambda a, b: op[(a, b)]
            return op
            
        add = make_callable(add_op)
        mul = make_callable(mul_op)
        
        # Check H1: R is a Boolean ring
        h1_ok = True
        for a in elements:
            if add(a, zero) != a: h1_ok = False; break
            if add(zero, a) != a: h1_ok = False; break
            if add(a, a) != zero: h1_ok = False; break
            if mul(a, a) != a: h1_ok = False; break
            for b in elements:
                if add(a, b) not in elements: h1_ok = False; break
                if mul(a, b) not in elements: h1_ok = False; break
                if add(a, b) != add(b, a): h1_ok = False; break
                if mul(a, b) != mul(b, a): h1_ok = False; break
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): h1_ok = False; break
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): h1_ok = False; break
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): h1_ok = False; break
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): h1_ok = False; break
                if not h1_ok: break
            if not h1_ok: break
        h1 = h1_ok
        
    except Exception:
        h1 = False

    try:
        # Check neg_Q: It is NOT the case that there exist unique a, b in R 
        # such that x = a + b, a in (y), and by = 0
        
        # Compute the principal ideal (y) in R
        ideal_y = []
        for r in elements:
            try:
                ry = mul(r, y)
                if ry not in ideal_y: 
                    ideal_y.append(ry)
                ry_plus_y = add(ry, y)
                if ry_plus_y not in ideal_y: 
                    ideal_y.append(ry_plus_y)
            except Exception:
                pass
                
        solutions = []
        for a in elements:
            for b in elements:
                try:
                    cond1 = (add(a, b) == x)
                    cond2 = (a in ideal_y)
                    cond3 = (mul(b, y) == zero)
                    if cond1 and cond2 and cond3:
                        solutions.append((a, b))
                except Exception:
                    pass
                    
        neg_q = (len(solutions) != 1)
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: It is not the case that there exist unique a, b in R such that x = a + b, a in (y), and by = 0"
]

N_HYP = 1
NEG_Q_INDEX = 1