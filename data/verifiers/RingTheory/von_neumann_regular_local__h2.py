import sympy
import sympy.ntheory
import itertools

# Top-level setup: named object bindings
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z10 = 10
Z12 = 12
Z15 = 15

def is_int_like(w):
    # Check if w is a Python int or a Sympy Integer, excluding booleans
    if isinstance(w, bool):
        return False
    return isinstance(w, int) or (hasattr(w, 'is_Integer') and w.is_Integer)

def to_int(w):
    return int(w)

def is_int_seq(w):
    return isinstance(w, (tuple, list)) and all(is_int_like(x) for x in w)

def get_ring_ops(witness):
    if is_int_like(witness):
        n = to_int(witness)
        if n <= 1:
            raise ValueError("n must be > 1")
        elements = list(range(n))
        add = lambda x, y: (x + y) % n
        mul = lambda x, y: (x * y) % n
        zero = 0
        one = 1 % n
        return elements, add, mul, zero, one
    elif is_int_seq(witness):
        elements = list(itertools.product(*[range(to_int(ni)) for ni in witness]))
        def add(x, y):
            return tuple((xi + yi) % to_int(ni) for xi, yi, ni in zip(x, y, witness))
        def mul(x, y):
            return tuple((xi * yi) % to_int(ni) for xi, yi, ni in zip(x, y, witness))
        zero = tuple(0 for _ in witness)
        one = tuple(1 % to_int(ni) for ni in witness)
        return elements, add, mul, zero, one
    else:
        elements = list(witness.elements)
        add = witness.add
        mul = witness.mul
        zero = witness.zero
        one = witness.one
        return elements, add, mul, zero, one

def is_commutative_ring(witness):
    if is_int_like(witness):
        return to_int(witness) > 1
    if is_int_seq(witness):
        return all(to_int(x) > 1 for x in witness) and len(witness) > 0
    
    elements, add, mul, zero, one = get_ring_ops(witness)
    n = len(elements)
    if n == 0: 
        return False
        
    for a in elements:
        if add(a, zero) != a: return False
        if mul(a, one) != a: return False
        if mul(one, a) != a: return False
        for b in elements:
            if add(a, b) != add(b, a): return False
            if mul(a, b) != mul(b, a): return False
            
    if n <= 50:
        for a in elements:
            for b in elements:
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
    return True

def is_von_neumann_regular(witness):
    if is_int_like(witness):
        n = to_int(witness)
        if n <= 1: return False
        for a in range(n):
            if not any((a * a * x) % n == a for x in range(n)):
                return False
        return True
    if is_int_seq(witness):
        for x in witness:
            n = to_int(x)
            if n <= 1: return False
            for a in range(n):
                if not any((a * a * x) % n == a for x in range(n)):
                    return False
        return True

    elements, add, mul, zero, one = get_ring_ops(witness)
    for a in elements:
        a_sq = mul(a, a)
        found = False
        for x in elements:
            if mul(a_sq, x) == a:
                found = True
                break
        if not found:
            return False
    return True

def is_field(witness):
    if is_int_like(witness):
        return sympy.isprime(to_int(witness))
    if is_int_seq(witness):
        if len(witness) == 1:
            return sympy.isprime(to_int(witness[0]))
        return False

    if not is_commutative_ring(witness):
        return False

    elements, add, mul, zero, one = get_ring_ops(witness)
    if zero == one:
        return False
    for a in elements:
        if a == zero:
            continue
        found = False
        for x in elements:
            if mul(a, x) == one:
                found = True
                break
        if not found:
            return False
    return True

def conditions(witness):
    try:
        h1 = is_commutative_ring(witness)
    except Exception:
        h1 = False

    try:
        h2 = is_von_neumann_regular(witness)
    except Exception:
        h2 = False

    try:
        neg_q = not is_field(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a von Neumann regular ring",
    "¬Q: R is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2