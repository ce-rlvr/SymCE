import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(ring_add):
    if isinstance(ring_add, dict):
        return list(ring_add.keys())
    return list(range(len(ring_add)))

def op(table, x, y):
    if isinstance(table, dict):
        return table[x][y]
    return table[x][y]

def find_zero(add_table, elements):
    for e in elements:
        if all(op(add_table, e, x) == x for x in elements) and \
           all(op(add_table, x, e) == x for x in elements):
            return e
    return None

def get_neg(add_table, elements, zero, x):
    for e in elements:
        if op(add_table, x, e) == zero and op(add_table, e, x) == zero:
            return e
    return None

def is_homomorphism(R_add, R_mul, S_add, S_mul, R_elems, S_elems, f):
    def apply_f(x):
        if isinstance(f, dict): return f[x]
        elif callable(f): return f(x)
        return f[x]
        
    for x in R_elems:
        try:
            fx = apply_f(x)
            if fx not in S_elems: return False
        except Exception:
            return False
            
    for x in R_elems:
        for y in R_elems:
            fx = apply_f(x)
            fy = apply_f(y)
            f_add = apply_f(op(R_add, x, y))
            f_mul = apply_f(op(R_mul, x, y))
            if f_add != op(S_add, fx, fy): return False
            if f_mul != op(S_mul, fx, fy): return False
            
    return True

def is_ideal(add_table, mul_table, elements, J):
    if not J: return False
    zero = find_zero(add_table, elements)
    if zero is None or zero not in J: return False
    
    for x in J:
        for y in J:
            neg_y = get_neg(add_table, elements, zero, y)
            if neg_y is None: return False
            if op(add_table, x, neg_y) not in J: return False
            
    for x in J:
        for s in elements:
            if op(mul_table, x, s) not in J: return False
            if op(mul_table, s, x) not in J: return False
            
    return True

def extract_witness(witness):
    if isinstance(witness, dict):
        return (witness['R_add'], witness['R_mul'], witness['S_add'], witness['S_mul'], witness['f'], witness['J'])
    elif isinstance(witness, tuple) or isinstance(witness, list):
        return witness
    else:
        return (witness.R_add, witness.R_mul, witness.S_add, witness.S_mul, witness.f, witness.J)

def conditions(witness) -> list[bool]:
    try:
        R_add, R_mul, S_add, S_mul, f, J = extract_witness(witness)
        R_elems = get_elements(R_add)
        S_elems = get_elements(S_add)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_homomorphism(R_add, R_mul, S_add, S_mul, R_elems, S_elems, f)
    except Exception:
        h1 = False
        
    try:
        J_list = list(J)
        h2 = is_ideal(S_add, S_mul, S_elems, J_list)
    except Exception:
        h2 = False
        
    try:
        def apply_f(x):
            if isinstance(f, dict): return f[x]
            elif callable(f): return f(x)
            return f[x]
            
        preimage = [x for x in R_elems if apply_f(x) in J_list]
        
        zero_S = find_zero(S_add, S_elems)
        ker_f = [x for x in R_elems if apply_f(x) == zero_S]
        
        is_preimage_ideal = is_ideal(R_add, R_mul, R_elems, preimage)
        contains_ker = all(x in preimage for x in ker_f)
        
        q = is_preimage_ideal and contains_ker
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: J is an ideal of S",
    "¬Q: The preimage f^{-1}(J) is not an ideal of R or does not contain ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2