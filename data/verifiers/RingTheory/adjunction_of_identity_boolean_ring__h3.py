import sympy
import itertools
import functools

CONDITION_LABELS = [
    "H_1: R is a Boolean ring without an identity element",
    "¬Q: R' is not a Boolean ring with identity (0, 1) or does not contain a subring isomorphic to R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    try:
        elements = witness.elements
        if callable(elements):
            elements = list(elements())
        else:
            elements = list(elements)
            
        zero = witness.zero
        if callable(zero):
            zero = zero()
            
        if hasattr(witness, 'add'):
            add_op = witness.add
            mul_op = witness.mul
        else:
            add_op = lambda a, b: a + b
            mul_op = lambda a, b: a * b
            
        is_bool = True
        for x in elements:
            if mul_op(x, x) != x:
                is_bool = False
                break
                
        if is_bool:
            is_ring = True
            for a in elements:
                if add_op(a, zero) != a: is_ring = False
                if add_op(a, a) != zero: is_ring = False
                for b in elements:
                    if add_op(a, b) != add_op(b, a): is_ring = False
                    if mul_op(a, b) != mul_op(b, a): is_ring = False
            
            if is_ring:
                for a in elements:
                    for b in elements:
                        for c in elements:
                            if add_op(add_op(a, b), c) != add_op(a, add_op(b, c)): is_ring = False
                            if mul_op(mul_op(a, b), c) != mul_op(a, mul_op(b, c)): is_ring = False
                            if mul_op(a, add_op(b, c)) != add_op(mul_op(a, b), mul_op(a, c)): is_ring = False
                            
            if is_ring:
                has_id = False
                for e in elements:
                    is_id = True
                    for a in elements:
                        if mul_op(e, a) != a:
                            is_id = False
                            break
                    if is_id:
                        has_id = True
                        break
                
                if not has_id:
                    h1 = True
    except Exception:
        pass

    q = False
    try:
        elements = witness.elements
        if callable(elements):
            elements = list(elements())
        else:
            elements = list(elements)
            
        zero = witness.zero
        if callable(zero):
            zero = zero()
            
        if hasattr(witness, 'add'):
            add_op = witness.add
            mul_op = witness.mul
        else:
            add_op = lambda a, b: a + b
            mul_op = lambda a, b: a * b
            
        R_prime = [(a, m) for a in elements for m in (0, 1)]
        
        def rp_add(x, y):
            return (add_op(x[0], y[0]), (x[1] + y[1]) % 2)
            
        def rp_mul(x, y):
            a, m = x
            b, n = y
            term1 = mul_op(a, b)
            term2 = a if n == 1 else zero
            term3 = b if m == 1 else zero
            first = add_op(add_op(term1, term2), term3)
            second = (m * n) % 2
            return (first, second)
            
        is_bool_prime = True
        for x in R_prime:
            if rp_mul(x, x) != x:
                is_bool_prime = False
                break
                
        id_elem = (zero, 1)
        has_id_prime = True
        for x in R_prime:
            if rp_mul(x, id_elem) != x or rp_mul(id_elem, x) != x:
                has_id_prime = False
                break
                
        # A subring must contain the identity of the parent ring.
        # The identity of R' is (zero, 1).
        # Since R has no identity, it cannot be isomorphic to any subring of R' 
        # (which would necessarily contain (zero, 1) and thus have an identity).
        contains_subring = False
        
        q = is_bool_prime and has_id_prime and contains_subring
    except Exception:
        pass

    return [h1, not q]