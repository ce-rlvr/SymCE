import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools

# Standard group bindings
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

# Standard matrix bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract_witness(witness):
    if isinstance(witness, dict):
        R = witness.get('R')
        add = witness.get('add')
        mul = witness.get('mul')
        I = witness.get('I')
        J = witness.get('J')
        return R, add, mul, I, J
    elif isinstance(witness, tuple):
        if len(witness) == 5:
            return witness
        elif len(witness) == 3:
            return witness[0], None, None, witness[1], witness[2]
    elif hasattr(witness, 'R') and hasattr(witness, 'I') and hasattr(witness, 'J'):
        add = getattr(witness, 'add', None)
        mul = getattr(witness, 'mul', None)
        return witness.R, add, mul, witness.I, witness.J
    return None, None, None, None, None

def get_a(add, R, x, y):
    if callable(add): return add(x, y)
    if isinstance(add, dict): return add.get((x, y), add.get(x, {}).get(y))
    idx_x = R.index(x)
    idx_y = R.index(y)
    return add[idx_x][idx_y]

def get_m(mul, R, x, y):
    if callable(mul): return mul(x, y)
    if isinstance(mul, dict): return mul.get((x, y), mul.get(x, {}).get(y))
    idx_x = R.index(x)
    idx_y = R.index(y)
    return mul[idx_x][idx_y]

def evaluate_ops(R, add, mul):
    def check(a, m):
        try:
            for x in R:
                if m(x, x) != x: return False
                for y in R:
                    if a(x, y) not in R: return False
                    if m(x, y) not in R: return False
            return True
        except Exception:
            return False

    if add is not None and mul is not None:
        a = lambda x, y: get_a(add, R, x, y)
        m = lambda x, y: get_m(mul, R, x, y)
        if check(a, m): return a, m
        return a, m

    # Try ^ and & (bitwise operations for sets/integers)
    a = lambda x, y: x ^ y
    m = lambda x, y: x & y
    if check(a, m): return a, m

    # Try + and *
    a = lambda x, y: x + y
    m = lambda x, y: x * y
    if check(a, m): return a, m
    
    # Try sympy Add and Mul
    a = lambda x, y: sympy.Add(x, y)
    m = lambda x, y: sympy.Mul(x, y)
    if check(a, m): return a, m

    return None, None

def conditions(witness) -> list[bool]:
    R, add, mul, I, J = extract_witness(witness)
    
    h1 = False
    a = None
    m = None
    try:
        if R is not None:
            R_list = list(R)
            a, m = evaluate_ops(R_list, add, mul)
            if a is not None and m is not None:
                is_ring = True
                
                # Closure
                for x in R_list:
                    for y in R_list:
                        if a(x, y) not in R_list: is_ring = False
                        if m(x, y) not in R_list: is_ring = False
                
                if is_ring:
                    # Commutativity of addition
                    for x in R_list:
                        for y in R_list:
                            if a(x, y) != a(y, x): is_ring = False
                            
                    # Associativity of addition and multiplication
                    for x in R_list:
                        for y in R_list:
                            for z in R_list:
                                if a(a(x, y), z) != a(x, a(y, z)): is_ring = False
                                if m(m(x, y), z) != m(x, m(y, z)): is_ring = False
                                
                    # Additive identity
                    zeros_list = [z for z in R_list if all(a(z, x) == x for x in R_list)]
                    if len(zeros_list) != 1:
                        is_ring = False
                    else:
                        zero = zeros_list[0]
                        # Additive inverse
                        for x in R_list:
                            if not any(a(x, y) == zero for y in R_list): is_ring = False
                            
                    # Distributivity
                    for x in R_list:
                        for y in R_list:
                            for z in R_list:
                                if m(x, a(y, z)) != a(m(x, y), m(x, z)): is_ring = False
                                if m(a(y, z), x) != a(m(y, x), m(z, x)): is_ring = False
                                
                    # Boolean condition (x^2 = x)
                    for x in R_list:
                        if m(x, x) != x: is_ring = False
                        
                h1 = is_ring
    except Exception:
        h1 = False

    neg_q = False
    try:
        if h1 and I is not None and J is not None and a is not None and m is not None:
            I_list = list(I)
            J_list = list(J)
            
            # Compute I \cap J
            try:
                I_cap_J = set(I_list).intersection(set(J_list))
            except TypeError:
                # Fallback for unhashable types
                I_cap_J = []
                for x in I_list:
                    if x in J_list and x not in I_cap_J:
                        I_cap_J.append(x)
            
            # Compute IJ (additive closure of products)
            products = []
            for i in I_list:
                for j in J_list:
                    p = m(i, j)
                    if p not in products:
                        products.append(p)
                        
            closure = list(products)
            added = True
            while added:
                added = False
                new_elements = []
                for x in closure:
                    for y in closure:
                        s = a(x, y)
                        if s not in closure and s not in new_elements:
                            new_elements.append(s)
                if new_elements:
                    closure.extend(new_elements)
                    added = True
                    
            # Compare closure and I_cap_J
            def is_equal(A, B):
                for x in A:
                    if x not in B: return False
                for x in B:
                    if x not in A: return False
                return True
                
            if not is_equal(closure, I_cap_J):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: IJ != I \\cap J"
]

N_HYP = 1
NEG_Q_INDEX = 1