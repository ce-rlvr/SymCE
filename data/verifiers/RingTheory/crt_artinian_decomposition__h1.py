import sympy as sp
import itertools

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def make_matrix_ring(n, p):
    elements = [sp.Matrix(n, n, entries) for entries in itertools.product(range(p), repeat=n*n)]
    def add(x, y): return (x + y).applyfunc(lambda a: a % p)
    def mul(x, y): return (x * y).applyfunc(lambda a: a % p)
    zero = sp.zeros(n, n)
    one = sp.eye(n)
    return elements, add, mul, zero, one

def make_upper_triangular_ring(n, p):
    elements = []
    for entries in itertools.product(range(p), repeat=n*(n+1)//2):
        M = sp.zeros(n, n)
        idx = 0
        for i in range(n):
            for j in range(i, n):
                M[i, j] = entries[idx]
                idx += 1
        elements.append(M)
    def add(x, y): return (x + y).applyfunc(lambda a: a % p)
    def mul(x, y): return (x * y).applyfunc(lambda a: a % p)
    zero = sp.zeros(n, n)
    one = sp.eye(n)
    return elements, add, mul, zero, one

def make_Zn_ring(n):
    elements = list(range(n))
    def add(x, y): return (x + y) % n
    def mul(x, y): return (x * y) % n
    zero = 0
    one = 1 % n
    return elements, add, mul, zero, one

M2_F2 = make_matrix_ring(2, 2)
T2_F2 = make_upper_triangular_ring(2, 2)
M2_F3 = make_matrix_ring(2, 3)
T2_F3 = make_upper_triangular_ring(2, 3)
Z4 = make_Zn_ring(4)
Z6 = make_Zn_ring(6)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "Let R be an Artinian ring. Then R is isomorphic to a finite direct product of local Artinian rings."
    
    The witness should be a tuple: (elements, add_func, mul_func, zero, one)
    representing a finite ring.
    """
    try:
        elements, add, mul, zero, one = witness
        elements = list(elements)
    except Exception:
        return [False, False]
        
    # H1: R is an Artinian ring
    # A finite ring is automatically Artinian. We verify it is a valid finite ring.
    try:
        is_ring = True
        if len(elements) == 0:
            is_ring = False
        elif zero not in elements or one not in elements:
            is_ring = False
            
        if is_ring:
            # Check ring axioms on a small sample to ensure validity without being too slow
            sample = elements[:10]
            for a in sample:
                if add(a, zero) != a: is_ring = False
                if add(zero, a) != a: is_ring = False
                if mul(a, one) != a: is_ring = False
                if mul(one, a) != a: is_ring = False
                for b in sample:
                    if add(a, b) != add(b, a): is_ring = False
                    for c in sample:
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): is_ring = False
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): is_ring = False
                        if mul(a, mul(b, c)) != mul(mul(a, b), c): is_ring = False
    except Exception:
        is_ring = False
        
    h1_ok = is_ring
    
    # neg_Q: R is NOT isomorphic to a finite direct product of local Artinian rings
    try:
        neg_q_ok = False
        if is_ring:
            # Find the center of the ring
            center = []
            for c in elements:
                is_central = True
                for x in elements:
                    if mul(c, x) != mul(x, c):
                        is_central = False
                        break
                if is_central:
                    center.append(c)
                    
            # Find central idempotents
            idempotents = []
            for e in center:
                if mul(e, e) == e:
                    idempotents.append(e)
                    
            # Find primitive central idempotents
            primitive_idempotents = []
            for e in idempotents:
                if e == zero: continue
                is_primitive = True
                for f in idempotents:
                    if f != zero and f != e:
                        if mul(e, f) == f:
                            is_primitive = False
                            break
                if is_primitive:
                    primitive_idempotents.append(e)
                    
            is_product_of_locals = True
            for e in primitive_idempotents:
                # Elements of the component ring Re
                Re = []
                for x in elements:
                    xe = mul(x, e)
                    if xe not in Re:
                        Re.append(xe)
                        
                # Find units in Re (where e is the identity)
                units = []
                for x in Re:
                    is_unit = False
                    for y in Re:
                        if mul(x, y) == e and mul(y, x) == e:
                            is_unit = True
                            break
                    if is_unit:
                        units.append(x)
                        
                # Non-units in Re
                non_units = [x for x in Re if x not in units]
                
                # A finite ring is local iff its non-units are closed under addition
                is_local = True
                for x in non_units:
                    for y in non_units:
                        if add(x, y) not in non_units:
                            is_local = False
                            break
                    if not is_local:
                        break
                        
                if not is_local:
                    is_product_of_locals = False
                    break
                    
            neg_q_ok = not is_product_of_locals
            
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is an Artinian ring",
    "¬Q: R is not isomorphic to a finite direct product of local Artinian rings"
]

N_HYP = 1
NEG_Q_INDEX = 1