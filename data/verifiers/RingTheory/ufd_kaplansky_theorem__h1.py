import math
from itertools import product

# Top-level setup: named object bindings for common finite rings
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

CONDITION_LABELS = [
    "H_1: Every non-zero prime ideal in R contains a non-zero prime element",
    "¬Q: R is not a unique factorization domain"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_ring(witness):
    """
    Constructs a finite ring Z/nZ or a direct product of such rings.
    Returns a dictionary with ring operations and properties, or None if invalid.
    """
    try:
        if hasattr(witness, '__iter__'):
            moduli = [int(m) for m in witness]
        else:
            moduli = [int(witness)]
            
        if any(m < 2 for m in moduli):
            return None
            
        # Limit size to prevent performance issues
        size = 1
        for m in moduli:
            size *= m
        if size > 400:
            return None
            
        elements = list(product(*[range(m) for m in moduli]))
        
        def add(x, y):
            return tuple((a + b) % m for a, b, m in zip(x, y, moduli))
            
        def mul(x, y):
            return tuple((a * b) % m for a, b, m in zip(x, y, moduli))
            
        zero = tuple(0 for _ in moduli)
        one = tuple(1 for _ in moduli)
        
        divides_memo = {}
        def divides(x, y):
            if (x, y) in divides_memo:
                return divides_memo[(x, y)]
            for k in elements:
                if mul(x, k) == y:
                    divides_memo[(x, y)] = True
                    return True
            divides_memo[(x, y)] = False
            return False

        def is_unit(x):
            return divides(x, one)
            
        def is_prime_element(x):
            if x == zero: return False
            if is_unit(x): return False
            for a in elements:
                for b in elements:
                    if divides(x, mul(a, b)):
                        if not divides(x, a) and not divides(x, b):
                            return False
            return True

        # In a finite product of Z/nZ, every ideal is principal.
        ideals = []
        for x in elements:
            ideal = set()
            for k in elements:
                ideal.add(mul(x, k))
            ideal_tuple = tuple(sorted(list(ideal)))
            if ideal_tuple not in ideals:
                ideals.append(ideal_tuple)
                
        prime_ideals = []
        for I_tuple in ideals:
            if len(I_tuple) == len(elements):
                continue  # Prime ideals must be proper
            I_set = set(I_tuple)
            is_prime = True
            for a in elements:
                for b in elements:
                    if mul(a, b) in I_set:
                        if a not in I_set and b not in I_set:
                            is_prime = False
                            break
                if not is_prime:
                    break
            if is_prime:
                prime_ideals.append(I_tuple)
                
        return {
            'elements': elements,
            'zero': zero,
            'one': one,
            'add': add,
            'mul': mul,
            'divides': divides,
            'is_unit': is_unit,
            'is_prime_element': is_prime_element,
            'ideals': ideals,
            'prime_ideals': prime_ideals
        }
    except Exception:
        return None

def conditions(witness):
    try:
        ring = get_ring(witness)
        if ring is None:
            return [False, False]
            
        # H_1: Every non-zero prime ideal in R contains a non-zero prime element
        h1_ok = True
        for I in ring['prime_ideals']:
            # Skip the zero ideal
            if len(I) == 1 and I[0] == ring['zero']:
                continue
            
            contains_prime = False
            for x in I:
                if x != ring['zero'] and ring['is_prime_element'](x):
                    contains_prime = True
                    break
            if not contains_prime:
                h1_ok = False
                break
                
        # Q: R is a unique factorization domain
        # A UFD must be an integral domain. For finite rings, being an integral domain
        # is equivalent to being a field, which is always a UFD.
        # Thus, a finite ring is a UFD if and only if it is an integral domain.
        is_domain = True
        for a in ring['elements']:
            if a == ring['zero']: continue
            for b in ring['elements']:
                if b == ring['zero']: continue
                if ring['mul'](a, b) == ring['zero']:
                    is_domain = False
                    break
            if not is_domain:
                break
                
        is_ufd = is_domain
        neg_q_ok = not is_ufd
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]