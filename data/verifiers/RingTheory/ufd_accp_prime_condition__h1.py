import sympy
import math
import itertools
import functools

# Standard bindings that might be used as witnesses
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
Z2xZ2 = (2, 2)
Z2xZ3 = (2, 3)

def conditions(witness):
    """
    Given a witness (representing a finite ring Z/nZ or a direct product of such rings),
    check if it satisfies the hypotheses and fails the conclusion.
    """
    try:
        if isinstance(witness, (tuple, list)):
            ns = tuple(int(x) for x in witness)
            if any(n < 2 for n in ns): 
                return [False, False, False]
            if math.prod(ns) > 500: 
                return [False, False, False]
            
            elements = list(itertools.product(*(range(n) for n in ns)))
            zero = tuple(0 for _ in ns)
            one = tuple(1 for _ in ns)
            
            def add(x, y): 
                return tuple((a + b) % n for a, b, n in zip(x, y, ns))
            
            def mul(x, y): 
                return tuple((a * b) % n for a, b, n in zip(x, y, ns))
            
            def is_domain():
                if len(ns) > 1: 
                    return False
                return sympy.isprime(ns[0])
            
            def is_unit(x):
                return all(math.gcd(a, n) == 1 for a, n in zip(x, ns))
                
        else:
            n = int(witness)
            if n < 2: 
                return [False, False, False]
            if n > 500: 
                return [False, False, False]
            
            elements = list(range(n))
            zero = 0
            one = 1
            
            def add(x, y): 
                return (x + y) % n
            
            def mul(x, y): 
                return (x * y) % n
            
            def is_domain(): 
                return sympy.isprime(n)
            
            def is_unit(x):
                return math.gcd(x, n) == 1
                
    except Exception:
        return [False, False, False]

    # H_1: R satisfies the ascending chain condition on principal ideals (ACCP)
    # Any finite ring is Artinian, hence Noetherian, and thus satisfies ACCP.
    h1_ok = True

    # H_2: Every irreducible element in R is a prime element
    try:
        non_units = [x for x in elements if not is_unit(x)]

        def is_irreducible(a):
            if a == zero: return False
            if is_unit(a): return False
            # a is irreducible if a = b*c implies b is a unit or c is a unit.
            # Equivalently, a cannot be written as the product of two non-units.
            for b in non_units:
                for c in non_units:
                    if mul(b, c) == a:
                        return False
            return True

        def is_prime_element(a):
            if a == zero: return False
            if is_unit(a): return False
            multiples = set(mul(a, k) for k in elements)
            non_multiples = [x for x in elements if x not in multiples]
            # a is prime if a | bc implies a | b or a | c.
            # Equivalently, if b and c are not multiples of a, then bc is not a multiple of a.
            for b in non_multiples:
                for c in non_multiples:
                    if mul(b, c) in multiples:
                        return False
            return True

        h2_ok = True
        for a in elements:
            if is_irreducible(a):
                if not is_prime_element(a):
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False

    # neg_Q: R is NOT a unique factorization domain
    # A UFD must be an integral domain. For finite rings, an integral domain is a field.
    # So a finite ring is a UFD if and only if it is an integral domain.
    try:
        neg_q_ok = not is_domain()
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R satisfies the ascending chain condition on principal ideals (ACCP)",
    "H_2: Every irreducible element in R is a prime element",
    "¬Q: R is not a unique factorization domain"
]

N_HYP = 2
NEG_Q_INDEX = 2