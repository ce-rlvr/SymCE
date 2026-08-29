import itertools
import math
from functools import reduce

# Top-level setup
# No specific named objects needed for Boolean rings, as they are typically constructed
# using integers and bitwise operations or subsets of power sets.

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            S = witness['S']
            f = witness['f']
            add_R = witness.get('add_R')
            mul_R = witness.get('mul_R')
            add_S = witness.get('add_S')
            mul_S = witness.get('mul_S')
        else:
            R = witness.R
            S = witness.S
            f = witness.f
            add_R = getattr(witness, 'add_R', None)
            mul_R = getattr(witness, 'mul_R', None)
            add_S = getattr(witness, 'add_S', None)
            mul_S = getattr(witness, 'mul_S', None)
    except Exception:
        return [False, False, False]

    def make_op(op, default_op):
        if op is not None:
            return op
        return default_op

    def default_add(x, y):
        if isinstance(x, int) and isinstance(y, int): return x ^ y
        if isinstance(x, tuple) and isinstance(y, tuple): return tuple(a ^ b for a, b in zip(x, y))
        if isinstance(x, (set, frozenset)) and isinstance(y, (set, frozenset)): return x ^ y
        raise ValueError("No default add for these types")

    def default_mul(x, y):
        if isinstance(x, int) and isinstance(y, int): return x & y
        if isinstance(x, tuple) and isinstance(y, tuple): return tuple(a & b for a, b in zip(x, y))
        if isinstance(x, (set, frozenset)) and isinstance(y, (set, frozenset)): return x & y
        raise ValueError("No default mul for these types")

    op_add_R = make_op(add_R, default_add)
    op_mul_R = make_op(mul_R, default_mul)
    op_add_S = make_op(add_S, default_add)
    op_mul_S = make_op(mul_S, default_mul)

    def eval_f(x):
        if isinstance(f, dict):
            if isinstance(x, set):
                try:
                    return f[x]
                except TypeError:
                    return f[frozenset(x)]
            return f[x]
        else:
            try:
                return f[x]
            except TypeError:
                return f(x)

    def is_boolean_ring(elements, add, mul):
        elements = list(elements)
        if not elements: return False
        
        # Closure
        for x in elements:
            for y in elements:
                if add(x, y) not in elements: return False
                if mul(x, y) not in elements: return False
                
        # Commutativity of addition
        for x in elements:
            for y in elements:
                if add(x, y) != add(y, x): return False
                
        # Associativity of addition
        for x in elements:
            for y in elements:
                for z in elements:
                    if add(add(x, y), z) != add(x, add(y, z)): return False
                    
        # Additive identity
        zero = None
        for e in elements:
            if all(add(x, e) == x for x in elements):
                zero = e
                break
        if zero is None: return False
        
        # Additive inverse (in Boolean rings, x + x = 0)
        for x in elements:
            if add(x, x) != zero: return False
            
        # Associativity of multiplication
        for x in elements:
            for y in elements:
                for z in elements:
                    if mul(mul(x, y), z) != mul(x, mul(y, z)): return False
                    
        # Distributivity
        for x in elements:
            for y in elements:
                for z in elements:
                    if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): return False
                    if mul(add(y, z), x) != add(mul(y, x), mul(z, x)): return False
                    
        # Boolean property (x^2 = x)
        for x in elements:
            if mul(x, x) != x: return False
            
        return True

    # H1: R and S are Boolean rings
    try:
        h1 = is_boolean_ring(R, op_add_R, op_mul_R) and is_boolean_ring(S, op_add_S, op_mul_S)
    except Exception:
        h1 = False

    # H2: f is a homomorphism from R to S
    try:
        h2 = True
        R_list = list(R)
        S_list = list(S)
        
        for x in R_list:
            fx = eval_f(x)
            if fx not in S_list:
                h2 = False
                break
                
        if h2:
            for x in R_list:
                for y in R_list:
                    if eval_f(op_add_R(x, y)) != op_add_S(eval_f(x), eval_f(y)):
                        h2 = False
                    if eval_f(op_mul_R(x, y)) != op_mul_S(eval_f(x), eval_f(y)):
                        h2 = False
                        
            # In the category of Boolean rings, homomorphisms must preserve the multiplicative identity (if it exists)
            def get_one(elements, mul):
                for e in elements:
                    if all(mul(x, e) == x and mul(e, x) == x for x in elements):
                        return e
                return None
            
            one_R = get_one(R_list, op_mul_R)
            one_S = get_one(S_list, op_mul_S)
            if one_R is not None and one_S is not None:
                if eval_f(one_R) != one_S:
                    h2 = False
    except Exception:
        h2 = False

    # ¬Q: The homomorphism f is not surjective
    try:
        image = []
        for x in list(R):
            fx = eval_f(x)
            if fx not in image:
                image.append(fx)
        
        neg_q = False
        for y in list(S):
            if y not in image:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are Boolean rings",
    "H_2: f is a homomorphism from R to S",
    "¬Q: The homomorphism f is not surjective"
]
N_HYP = 2
NEG_Q_INDEX = 2