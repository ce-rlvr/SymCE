import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol
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

CONDITION_LABELS = [
    "H_1: R is a local ring",
    "H_2: R is a von Neumann regular ring",
    "¬Q: R is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_prop(witness, prop_name):
    if isinstance(witness, dict) and prop_name in witness:
        val = witness[prop_name]
        return val() if callable(val) else val
    if hasattr(witness, prop_name):
        val = getattr(witness, prop_name)
        return val() if callable(val) else val
    return None

def add(a, b, witness):
    if hasattr(witness, 'add'):
        return witness.add(a, b)
    return a + b

def mul(a, b, witness):
    if hasattr(witness, 'mul'):
        return witness.mul(a, b)
    return a * b

def eq(a, b, witness):
    if hasattr(witness, 'eq'):
        return witness.eq(a, b)
    return a == b

def check_local(witness):
    prop = get_prop(witness, 'is_local')
    if prop is not None:
        return bool(prop)
        
    if isinstance(witness, str):
        if witness.lower() in ['quaternions', 'quaternion', 'h', 'quaternion algebra']:
            return True
            
    elements = list(witness.elements)
    zero = witness.zero
    one = witness.one
    
    if eq(zero, one, witness):
        return False
        
    def is_unit(x):
        has_left = any(eq(mul(y, x, witness), one, witness) for y in elements)
        has_right = any(eq(mul(x, y, witness), one, witness) for y in elements)
        return has_left and has_right

    non_units = [x for x in elements if not is_unit(x)]
    
    for x in non_units:
        for y in non_units:
            if is_unit(add(x, y, witness)):
                return False
                
    for x in non_units:
        for r in elements:
            if is_unit(mul(r, x, witness)) or is_unit(mul(x, r, witness)):
                return False
                
    return True

def check_vnr(witness):
    prop = get_prop(witness, 'is_von_neumann_regular')
    if prop is not None:
        return bool(prop)
        
    if isinstance(witness, str):
        if witness.lower() in ['quaternions', 'quaternion', 'h', 'quaternion algebra']:
            return True
            
    elements = list(witness.elements)
    for a in elements:
        a2 = mul(a, a, witness)
        if not any(eq(mul(a2, x, witness), a, witness) for x in elements):
            return False
    return True

def check_field(witness):
    prop = get_prop(witness, 'is_field')
    if prop is not None:
        return bool(prop)
        
    if isinstance(witness, str):
        if witness.lower() in ['quaternions', 'quaternion', 'h', 'quaternion algebra']:
            return False
            
    elements = list(witness.elements)
    zero = witness.zero
    one = witness.one
    
    if eq(zero, one, witness):
        return False
        
    for a in elements:
        for b in elements:
            if not eq(mul(a, b, witness), mul(b, a, witness), witness):
                return False
                
    for a in elements:
        if not eq(a, zero, witness):
            if not any(eq(mul(a, x, witness), one, witness) for x in elements):
                return False
                
    return True

def conditions(witness) -> list[bool]:
    try:
        h1 = check_local(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = check_vnr(witness)
    except Exception:
        h2 = False
        
    try:
        q = check_field(witness)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]