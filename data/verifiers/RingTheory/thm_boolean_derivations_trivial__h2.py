import itertools
import functools
import math
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3

# Top-level setup for potential witness references
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

def extract_witness(witness):
    if isinstance(witness, dict):
        return witness['R'], witness['add'], witness['mul'], witness['d']
    elif isinstance(witness, (tuple, list)) and len(witness) == 4:
        return witness[0], witness[1], witness[2], witness[3]
    elif hasattr(witness, 'R') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'd'):
        return witness.R, witness.add, witness.mul, witness.d
    elif hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'd'):
        return witness.elements(), witness.add, witness.mul, witness.d
    else:
        raise ValueError("Unrecognized witness format")

def conditions(witness) -> list[bool]:
    try:
        R, add, mul, d = extract_witness(witness)
    except Exception:
        return [False, False]
        
    def get_val2(op, x, y):
        if isinstance(op, dict):
            return op.get((x, y))
        elif isinstance(op, (list, tuple)):
            return op[x][y]
        return op(x, y)
        
    def get_val1(op, x):
        if isinstance(op, dict):
            return op.get(x)
        elif isinstance(op, (list, tuple)):
            return op[x]
        return op(x)

    # H1: R is a Boolean ring
    h1_ok = False
    zero = None
    try:
        R_list = list(R)
        if len(R_list) > 0:
            closed = True
            for x in R_list:
                for y in R_list:
                    if get_val2(add, x, y) not in R_list: closed = False
                    if get_val2(mul, x, y) not in R_list: closed = False
            
            if closed:
                assoc_add = all(get_val2(add, get_val2(add, x, y), z) == get_val2(add, x, get_val2(add, y, z)) 
                                for x in R_list for y in R_list for z in R_list)
                comm_add = all(get_val2(add, x, y) == get_val2(add, y, x) 
                               for x in R_list for y in R_list)
                
                for e in R_list:
                    if all(get_val2(add, e, x) == x for x in R_list):
                        zero = e
                        break
                        
                has_inv = False
                if zero is not None:
                    has_inv = all(any(get_val2(add, x, y) == zero for y in R_list) for x in R_list)
                    
                assoc_mul = all(get_val2(mul, get_val2(mul, x, y), z) == get_val2(mul, x, get_val2(mul, y, z)) 
                                for x in R_list for y in R_list for z in R_list)
                                
                dist = all(get_val2(mul, x, get_val2(add, y, z)) == get_val2(add, get_val2(mul, x, y), get_val2(mul, x, z)) and
                           get_val2(mul, get_val2(add, y, z), x) == get_val2(add, get_val2(mul, y, x), get_val2(mul, z, x))
                           for x in R_list for y in R_list for z in R_list)
                           
                bool_prop = all(get_val2(mul, x, x) == x for x in R_list)
                
                if assoc_add and comm_add and zero is not None and has_inv and assoc_mul and dist and bool_prop:
                    h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: d(x) != 0 for some x in R
    neg_q = False
    try:
        if h1_ok and zero is not None:
            for x in R_list:
                if get_val1(d, x) != zero:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: d(x) != 0 for some x in R"
]

N_HYP = 1
NEG_Q_INDEX = 1