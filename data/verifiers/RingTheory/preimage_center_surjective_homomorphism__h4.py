import sympy
from sympy import Rational, Integer
from sympy.matrices import eye, zeros
import itertools
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_list(w, name):
    if isinstance(w, dict):
        return list(w[name])
    return list(getattr(w, name))

def get_func(w, name):
    if isinstance(w, dict):
        val = w[name]
        if isinstance(val, dict):
            if len(val) > 0:
                first_key = next(iter(val.keys()))
                if isinstance(first_key, tuple):
                    return lambda x, y: val[(x, y)]
                else:
                    return lambda x: val[x]
            else:
                return lambda x: val[x]
        elif isinstance(val, (list, tuple)):
            if len(val) > 0 and isinstance(val[0], (list, tuple)):
                return lambda x, y: val[x][y]
            else:
                return lambda x: val[x]
        return val
    else:
        return getattr(w, name)

def is_ring(elements, add, mul):
    if not elements: 
        return False
    
    # Closure
    for x in elements:
        for y in elements:
            if add(x, y) not in elements: return False
            if mul(x, y) not in elements: return False
            
    # Additive identity
    zeros_list = []
    for z in elements:
        if all(add(z, x) == x and add(x, z) == x for x in elements):
            zeros_list.append(z)
    if not zeros_list: 
        return False
    zero = zeros_list[0]
    
    # Ring axioms
    for x in elements:
        # Additive inverse
        if not any(add(x, y) == zero and add(y, x) == zero for y in elements):
            return False
        for y in elements:
            # Commutativity of addition
            if add(x, y) != add(y, x): 
                return False
            for z in elements:
                # Associativity and Distributivity
                if add(add(x, y), z) != add(x, add(y, z)): return False
                if mul(mul(x, y), z) != mul(x, mul(y, z)): return False
                if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): return False
                if mul(add(x, y), z) != add(mul(x, z), mul(y, z)): return False
    return True

def is_surjective_hom(R, S, add_R, mul_R, add_S, mul_S, f):
    mapped = []
    for x in R:
        fx = f(x)
        if fx not in S: 
            return False
        mapped.append(fx)
        
    # Surjectivity
    for s in S:
        if s not in mapped: 
            return False
        
    # Homomorphism properties
    for x in R:
        for y in R:
            if f(add_R(x, y)) != add_S(f(x), f(y)): return False
            if f(mul_R(x, y)) != mul_S(f(x), f(y)): return False
            
    return True

def get_center(elements, mul):
    Z = []
    for x in elements:
        if all(mul(x, y) == mul(y, x) for y in elements):
            Z.append(x)
    return Z

def conditions(witness):
    try:
        R = get_list(witness, 'R')
        S = get_list(witness, 'S')
        add_R = get_func(witness, 'add_R')
        mul_R = get_func(witness, 'mul_R')
        add_S = get_func(witness, 'add_S')
        mul_S = get_func(witness, 'mul_S')
        f = get_func(witness, 'f')
    except Exception:
        return [False, False, False, False]

    # H_1: R and S are rings
    try:
        h1_ok = is_ring(R, add_R, mul_R) and is_ring(S, add_S, mul_S)
    except Exception:
        h1_ok = False

    # H_2: f is a surjective ring homomorphism
    try:
        h2_ok = is_surjective_hom(R, S, add_R, mul_R, add_S, mul_S, f)
    except Exception:
        h2_ok = False

    # H_3: Z(S) denotes the center of S (definitional)
    h3_ok = True

    # neg_Q: The preimage f^{-1}(Z(S)) is NOT a subring of R that contains both Z(R) and ker(f)
    try:
        Z_S = get_center(S, mul_S)
        preimage = [x for x in R if f(x) in Z_S]
        
        Z_R = get_center(R, mul_R)
        
        zeros_S = [z for z in S if all(add_S(z, x) == x and add_S(x, z) == x for x in S)]
        if not zeros_S:
            return [h1_ok, h2_ok, h3_ok, False]
        zero_S = zeros_S[0]
        ker_f = [x for x in R if f(x) == zero_S]
        
        zeros_R = [z for z in R if all(add_R(z, x) == x and add_R(x, z) == x for x in R)]
        if not zeros_R:
            return [h1_ok, h2_ok, h3_ok, False]
        zero_R = zeros_R[0]
        
        subring_ok = True
        if zero_R not in preimage:
            subring_ok = False
        else:
            for x in preimage:
                neg_x = None
                for y in R:
                    if add_R(x, y) == zero_R and add_R(y, x) == zero_R:
                        neg_x = y
                        break
                if neg_x not in preimage:
                    subring_ok = False
                    break
                for y in preimage:
                    if add_R(x, y) not in preimage:
                        subring_ok = False
                        break
                    if mul_R(x, y) not in preimage:
                        subring_ok = False
                        break
                        
        contains_Z_R = all(x in preimage for x in Z_R)
        contains_ker_f = all(x in preimage for x in ker_f)
        
        q_ok = subring_ok and contains_Z_R and contains_ker_f
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a surjective ring homomorphism",
    "H_3: Z(S) denotes the center of S",
    "¬Q: f^{-1}(Z(S)) is not a subring containing Z(R) and ker(f)"
]

N_HYP = 3
NEG_Q_INDEX = 3