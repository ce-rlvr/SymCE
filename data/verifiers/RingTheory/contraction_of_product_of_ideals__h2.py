import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
import itertools

def call_op(op, a, b):
    if callable(op):
        return op(a, b)
    elif isinstance(op, dict):
        return op[(a, b)]
    else:
        return op[a][b]

def call_f(f, val):
    if callable(f):
        return f(val)
    elif isinstance(f, dict):
        return f[val]
    else:
        return f[val]

def is_comm_ring(elements, add, mul):
    if not elements: 
        return False
    elements = list(elements)
    
    # Closure
    for a in elements:
        for b in elements:
            if call_op(add, a, b) not in elements: return False
            if call_op(mul, a, b) not in elements: return False
            
    # Commutativity
    for a in elements:
        for b in elements:
            if call_op(add, a, b) != call_op(add, b, a): return False
            if call_op(mul, a, b) != call_op(mul, b, a): return False
            
    # Associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if call_op(add, call_op(add, a, b), c) != call_op(add, a, call_op(add, b, c)): return False
                if call_op(mul, call_op(mul, a, b), c) != call_op(mul, a, call_op(mul, b, c)): return False
                
    # Distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if call_op(mul, a, call_op(add, b, c)) != call_op(add, call_op(mul, a, b), call_op(mul, a, c)): return False
                
    # Additive identity
    zero = None
    for e in elements:
        if all(call_op(add, e, val) == val for val in elements):
            zero = e
            break
    if zero is None: 
        return False
        
    # Additive inverses
    for val in elements:
        if not any(call_op(add, val, y) == zero for y in elements): return False
    
    # Multiplicative identity
    one = None
    for e in elements:
        if all(call_op(mul, e, val) == val for val in elements):
            one = e
            break
    if one is None: 
        return False
    
    return True

def get_zero(elements, add):
    for e in elements:
        if all(call_op(add, e, val) == val for val in elements):
            return e
    return None

def is_ideal(elements, add, mul, zero, I):
    if not I: 
        return False
    I = list(I)
    
    # Subset check
    for val in I:
        if val not in elements: return False
        
    # Closed under addition
    for a in I:
        for b in I:
            if call_op(add, a, b) not in I: return False
            
    # Closed under additive inverses
    for val in I:
        inv_val = [y for y in elements if call_op(add, val, y) == zero]
        if not any(y in I for y in inv_val): return False
        
    # Absorbing property
    for val in I:
        for r in elements:
            if call_op(mul, r, val) not in I: return False
            if call_op(mul, val, r) not in I: return False
            
    return True

def compute_IJ(elements, add, mul, I, J):
    products = []
    for a in I:
        for b in J:
            p = call_op(mul, a, b)
            if p not in products:
                products.append(p)
                
    closure = list(products)
    added = True
    while added:
        added = False
        new_elements = []
        for a in closure:
            for b in closure:
                c = call_op(add, a, b)
                if c not in closure and c not in new_elements and c in elements:
                    new_elements.append(c)
        if new_elements:
            closure.extend(new_elements)
            added = True
            if len(closure) >= len(elements):
                break
    return closure

def compute_product_ideal(elements, add, mul, A, B):
    products = []
    for a in A:
        for b in B:
            p = call_op(mul, a, b)
            if p not in products:
                products.append(p)
                
    closure = list(products)
    added = True
    while added:
        added = False
        new_elements = []
        for a in closure:
            for b in closure:
                c = call_op(add, a, b)
                if c not in closure and c not in new_elements and c in elements:
                    new_elements.append(c)
        if new_elements:
            closure.extend(new_elements)
            added = True
            if len(closure) >= len(elements):
                break
    return closure

def conditions(witness):
    """
    witness can be a dictionary with keys:
    'R', 'R_add', 'R_mul', 'S', 'S_add', 'S_mul', 'f', 'I', 'J'
    or a tuple in that exact order.
    """
    try:
        if isinstance(witness, dict):
            R = witness['R']
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            S = witness['S']
            S_add = witness['S_add']
            S_mul = witness['S_mul']
            f = witness['f']
            I = witness['I']
            J = witness['J']
        else:
            R, R_add, R_mul, S, S_add, S_mul, f, I, J = witness
    except Exception:
        return [False] * 5

    # H1: R is a commutative ring
    try:
        h1 = is_comm_ring(R, R_add, R_mul)
    except Exception:
        h1 = False

    # H2: S is a commutative ring
    try:
        h2 = is_comm_ring(S, S_add, S_mul)
    except Exception:
        h2 = False

    # H3: I is an ideal of S
    try:
        zeroS = get_zero(S, S_add)
        h3 = is_ideal(S, S_add, S_mul, zeroS, I)
    except Exception:
        h3 = False

    # H4: J is an ideal of S
    try:
        zeroS = get_zero(S, S_add)
        h4 = is_ideal(S, S_add, S_mul, zeroS, J)
    except Exception:
        h4 = False

    # neg_Q: f^{-1}(I)f^{-1}(J) is not a subset of f^{-1}(IJ)
    try:
        IJ = compute_IJ(S, S_add, S_mul, I, J)
        f_inv_I = [x for x in R if call_f(f, x) in I]
        f_inv_J = [x for x in R if call_f(f, x) in J]
        f_inv_IJ = [x for x in R if call_f(f, x) in IJ]
        
        prod_f_inv = compute_product_ideal(R, R_add, R_mul, f_inv_I, f_inv_J)
        
        is_subset = all(x in f_inv_IJ for x in prod_f_inv)
        neg_q = not is_subset
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a commutative ring",
    "H_3: I is an ideal of S",
    "H_4: J is an ideal of S",
    "¬Q: f^{-1}(I)f^{-1}(J) is not a subset of f^{-1}(IJ)"
]

N_HYP = 4
NEG_Q_INDEX = 4