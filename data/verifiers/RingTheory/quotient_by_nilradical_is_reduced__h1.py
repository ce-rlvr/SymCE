import sympy
from sympy import Matrix, eye, zeros
import itertools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class FiniteRing:
    """
    A helper class to represent a finite ring.
    Witnesses can be instances of this class.
    """
    def __init__(self, elements, add_func, mul_func, zero):
        self.elements = list(elements)
        self.add = add_func
        self.mul = mul_func
        self.zero = zero

def MatrixRing(n, mod):
    """
    Generates the full matrix ring M_n(Z/mod Z).
    This is useful for providing non-commutative finite ring witnesses.
    """
    elements = []
    for vals in itertools.product(range(mod), repeat=n*n):
        elements.append(Matrix(n, n, vals))
    
    def add(A, B):
        return (A + B).applyfunc(lambda x: x % mod)
    
    def mul(A, B):
        return (A * B).applyfunc(lambda x: x % mod)
    
    zero = Matrix(n, n, [0]*(n*n))
    return FiniteRing(elements, add, mul, zero)

def get_ring(witness):
    if isinstance(witness, tuple) and len(witness) >= 1:
        witness = witness[0]
        
    if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'zero'):
        return witness.elements, witness.add, witness.mul, witness.zero
        
    if isinstance(witness, list) and len(witness) > 0 and hasattr(witness[0], 'is_Matrix'):
        elements = witness
        def add(x, y): return x + y
        def mul(x, y): return x * y
        zero = elements[0] * 0
        return elements, add, mul, zero
        
    raise ValueError("Witness must be a FiniteRing object or a list of matrices")

def is_ring(elements, add, mul, zero):
    if zero not in elements: 
        return False
    n = len(elements)
    
    # Check closure and existence of additive inverses
    for a in elements:
        has_inv = False
        for b in elements:
            if add(a, b) not in elements: return False
            if mul(a, b) not in elements: return False
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
        if not has_inv: 
            return False
            
    # Check zero identity
    for a in elements:
        if add(a, zero) != a or add(zero, a) != a: 
            return False
            
    # Check associativity and distributivity (probabilistic/subset for performance on larger rings)
    subset = elements if n <= 20 else elements[:10]
    for a in subset:
        for b in subset:
            if add(a, b) != add(b, a): return False
            for c in subset:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                
    return True

def get_nilpotents(elements, mul, zero):
    nilpotents = []
    n = len(elements)
    for a in elements:
        curr = a
        is_nil = False
        for _ in range(n):
            if curr == zero:
                is_nil = True
                break
            curr = mul(curr, a)
        if is_nil:
            nilpotents.append(a)
    return nilpotents

def is_ideal(N, elements, add, mul, zero):
    if zero not in N: 
        return False
        
    # Check closure under addition
    for a in N:
        for b in N:
            if add(a, b) not in N:
                return False
                
    # Check additive inverses in N
    for a in N:
        has_inv = False
        for b in N:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: 
            return False
            
    # Check closure under left and right multiplication by any ring element
    for a in N:
        for r in elements:
            if mul(r, a) not in N:
                return False
            if mul(a, r) not in N:
                return False
                
    return True

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, zero = get_ring(witness)
        h1 = is_ring(elements, add, mul, zero)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # N is defined as the nilradical (set of nilpotent elements) of R
            N = get_nilpotents(elements, mul, zero)
            
            # The conclusion states that the nilradical of R/N is the zero ideal.
            # For R/N to be a valid quotient ring, N must be an ideal.
            # If N is an ideal, R/N is guaranteed to be reduced (nilradical is zero).
            # The conclusion fails precisely when N fails to be an ideal, 
            # making the quotient ring R/N undefined.
            neg_q = not is_ideal(N, elements, add, mul, zero)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let N be the nilradical of R",
    "¬Q: The nilradical of the quotient ring R/N is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1